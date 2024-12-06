from typing import Dict, List, Optional, Any, Type, Set
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
import asyncio
import uuid
import logging
from enum import Enum
from ..core.agent import Agent, AgentState

logger = logging.getLogger(__name__)

class RoutingStrategy(str, Enum):
    ROUND_ROBIN = "round_robin"
    LEAST_BUSY = "least_busy"
    CAPABILITY_BASED = "capability_based"
    PRIORITY = "priority"

class Route(BaseModel):
    """A route definition for task routing"""
    pattern: str
    agent_type: Type[Agent]
    capabilities: Set[str] = Field(default_factory=set)
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

class Task(BaseModel):
    """A task to be routed and executed"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: str
    content: Any
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

class RoutingConfig(BaseModel):
    """Configuration for the router"""
    strategy: RoutingStrategy = RoutingStrategy.ROUND_ROBIN
    max_queue_size: int = 1000
    default_timeout: float = 60.0

class AgentRouter:
    """Routes tasks to appropriate agents based on capabilities"""
    
    def __init__(self, config: RoutingConfig = RoutingConfig()):
        self.config = config
        self.routes: List[Route] = []
        self._tasks: Dict[str, Task] = {}
        self._results: Dict[str, Any] = {}
        self._agent_pool: Dict[str, Agent] = {}
        self._running_tasks: Dict[str, asyncio.Task] = {}
        self._running = False
        self._processing_task: Optional[asyncio.Task] = None
    
    def register_route(self, route: Route) -> None:
        """Register a new route"""
        self.routes.append(route)
        logger.info(f"Registered route for pattern '{route.pattern}'")
    
    def find_route(self, pattern: str) -> Optional[Route]:
        """Find a route matching the given pattern"""
        for route in self.routes:
            if self._pattern_matches(route.pattern, pattern):
                return route
        return None
    
    def _pattern_matches(self, route_pattern: str, task_pattern: str) -> bool:
        """Check if a task pattern matches a route pattern"""
        # Simple wildcard matching for now
        if route_pattern.endswith('*'):
            return task_pattern.startswith(route_pattern[:-1])
        return route_pattern == task_pattern
    
    async def submit_task(self, task: Task) -> str:
        """Submit a task for routing and execution"""
        self._tasks[task.id] = task
        logger.info(f"Submitted task {task.id} of type {task.type}")
        return task.id
    
    async def get_task_result(self, task_id: str, timeout: float = 60.0) -> Any:
        """Get the result of a task"""
        start_time = datetime.utcnow()
        while True:
            if task_id in self._results:
                result = self._results.pop(task_id)
                self._tasks.pop(task_id, None)
                return result
            
            if (datetime.utcnow() - start_time).total_seconds() > timeout:
                raise TimeoutError(f"Task {task_id} timed out")
            
            await asyncio.sleep(0.1)
    
    async def process_task(self, task_id: str) -> None:
        """Process a task by finding and executing the appropriate route"""
        task = self._tasks.get(task_id)
        if not task:
            logger.warning(f"Task {task_id} not found")
            return
        
        route = self.find_route(task.type)
        if not route:
            logger.warning(f"No route found for task type {task.type}")
            return
        
        try:
            agent = route.agent_type()
            await agent.initialize()
            result = await agent.execute(task.content)
            await agent.cleanup()
            
            self._results[task_id] = result
            logger.info(f"Task {task_id} completed successfully")
        
        except Exception as e:
            logger.error(f"Error processing task {task_id}: {str(e)}")
            self._results[task_id] = None
    
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
    
    async def _process_queue(self) -> None:
        """Process tasks from the queue"""
        while self._running:
            try:
                task_id = await asyncio.to_thread(self._tasks.keys().__iter__().__next__)
                task = self._tasks[task_id]
                processing_task = asyncio.create_task(self.process_task(task_id))
                self._running_tasks[task_id] = processing_task
                
                # Clean up completed tasks
                done_tasks = [
                    task_id for task_id, t in self._running_tasks.items()
                    if t.done()
                ]
                for task_id in done_tasks:
                    self._running_tasks.pop(task_id, None)
                
            except Exception as e:
                logger.error(f"Error processing task: {str(e)}")