from typing import Dict, List, Optional, Type, Any, Callable
from pydantic import BaseModel, Field, ConfigDict
import asyncio
import logging
from datetime import datetime
import uuid
from enum import Enum

from core.agent import BaseAgent, AgentState, TaskAgent
from core.executor import AgentExecutor, ExecutionResult

logger = logging.getLogger(__name__)

class RoutingStrategy(str, Enum):
    ROUND_ROBIN = "round_robin"
    LEAST_BUSY = "least_busy"
    CAPABILITY_BASED = "capability_based"
    PRIORITY = "priority"

class Route(BaseModel):
    """Defines a routing rule"""
    pattern: str  # Pattern to match against task
    agent_type: Type[BaseAgent]
    priority: int = 0
    capabilities: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

class RoutingConfig(BaseModel):
    """Configuration for the router"""
    strategy: RoutingStrategy = RoutingStrategy.ROUND_ROBIN
    max_queue_size: int = 1000
    default_timeout: float = 60.0

class Task(BaseModel):
    """Represents a task to be routed"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    input_data: Any
    pattern: str
    priority: int = 0
    required_capabilities: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AgentRouter:
    """Routes tasks to appropriate agents based on configured strategy"""
    
    def __init__(self, config: RoutingConfig = RoutingConfig()):
        self.config = config
        self.routes: List[Route] = []
        self.executor = AgentExecutor()
        self._task_queue: asyncio.Queue = asyncio.Queue(maxsize=config.max_queue_size)
        self._running_tasks: Dict[str, asyncio.Task] = {}
        self._agent_pool: Dict[str, BaseAgent] = {}
        self._route_handlers: Dict[str, List[Callable]] = {}
        self._running = False
        self._processing_task: Optional[asyncio.Task] = None
    
    def register_route(self, route: Route) -> None:
        """Register a new routing rule"""
        self.routes.append(route)
        self.routes.sort(key=lambda x: x.priority, reverse=True)
    
    def register_agent(self, agent: BaseAgent) -> None:
        """Register an agent in the pool"""
        self._agent_pool[agent.id] = agent
    
    def remove_agent(self, agent_id: str) -> None:
        """Remove an agent from the pool"""
        self._agent_pool.pop(agent_id, None)
    
    async def submit_task(self, task: Task) -> str:
        """Submit a task for routing"""
        await self._task_queue.put(task)
        return task.id
    
    async def get_task_result(self, task_id: str, timeout: Optional[float] = None) -> Optional[ExecutionResult]:
        """Get the result of a task"""
        timeout = timeout or self.config.default_timeout
        try:
            task = self._running_tasks.get(task_id)
            if task:
                return await asyncio.wait_for(task, timeout=timeout)
            return None
        except asyncio.TimeoutError:
            logger.warning(f"Timeout waiting for task {task_id}")
            raise
    
    def _find_matching_route(self, task: Task) -> Optional[Route]:
        """Find the first matching route for a task"""
        for route in self.routes:
            if self._matches_pattern(task.pattern, route.pattern):
                if all(cap in route.capabilities for cap in task.required_capabilities):
                    return route
        return None
    
    def _matches_pattern(self, task_pattern: str, route_pattern: str) -> bool:
        """Check if task pattern matches route pattern"""
        # Simple pattern matching for now, could be enhanced with regex
        return task_pattern.startswith(route_pattern.rstrip(".*"))
    
    async def _select_agent(self, agent_type: Type[BaseAgent], task: Task) -> Optional[BaseAgent]:
        """Select an agent based on the routing strategy"""
        available_agents = [
            agent for agent in self._agent_pool.values()
            if isinstance(agent, agent_type) and agent.state == AgentState.IDLE
        ]
        
        if not available_agents:
            # Create new agent instance if none available
            agent = agent_type(
                name=f"{agent_type.__name__}_{len(self._agent_pool)}",
                description=f"Dynamically created agent for task {task.id}"
            )
            self.register_agent(agent)
            return agent
        
        match self.config.strategy:
            case RoutingStrategy.ROUND_ROBIN:
                return available_agents[0]  # Simple round-robin
            case RoutingStrategy.LEAST_BUSY:
                return min(available_agents, key=lambda a: len(self._get_agent_tasks(a.id)))
            case RoutingStrategy.CAPABILITY_BASED:
                return next(
                    (a for a in available_agents if all(
                        cap in getattr(a, 'capabilities', [])
                        for cap in task.required_capabilities
                    )),
                    available_agents[0]
                )
            case RoutingStrategy.PRIORITY:
                return max(available_agents, key=lambda a: getattr(a, 'priority', 0))
    
    def _get_agent_tasks(self, agent_id: str) -> List[str]:
        """Get tasks currently assigned to an agent"""
        return [
            task_id for task_id, task in self._running_tasks.items()
            if getattr(task, 'agent_id', None) == agent_id
        ]
    
    async def _process_task(self, task: Task) -> ExecutionResult:
        """Process a single task"""
        route = self._find_matching_route(task)
        if not route:
            raise ValueError(f"No matching route found for task {task.id}")
        
        agent = await self._select_agent(route.agent_type, task)
        if not agent:
            raise ValueError(f"No available agent found for task {task.id}")
        
        try:
            result = await self.executor.execute_agent(agent, task.input_data)
            return result
        except Exception as e:
            logger.error(f"Error executing task {task.id}: {str(e)}")
            raise
    
    async def _process_queue(self) -> None:
        """Process tasks from the queue"""
        while self._running:
            try:
                task = await self._task_queue.get()
                processing_task = asyncio.create_task(self._process_task(task))
                self._running_tasks[task.id] = processing_task
                
                # Clean up completed tasks
                done_tasks = [
                    task_id for task_id, t in self._running_tasks.items()
                    if t.done()
                ]
                for task_id in done_tasks:
                    self._running_tasks.pop(task_id, None)
                
            except Exception as e:
                logger.error(f"Error processing task: {str(e)}")
    
    async def start(self) -> None:
        """Start the router"""
        if self._running:
            return
        
        self._running = True
        self._processing_task = asyncio.create_task(self._process_queue())
    
    async def stop(self) -> None:
        """Stop the router and clean up resources"""
        self._running = False
        if self._processing_task:
            self._processing_task.cancel()
            try:
                await self._processing_task
            except asyncio.CancelledError:
                pass
        
        for task in self._running_tasks.values():
            task.cancel()
        
        await self.executor.shutdown()