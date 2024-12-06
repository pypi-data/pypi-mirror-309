from typing import Dict, List, Any, Optional, Type
from concurrent.futures import ThreadPoolExecutor
import asyncio
from datetime import datetime
import logging
from pydantic import BaseModel, Field

from .agent import BaseAgent, AgentState

logger = logging.getLogger(__name__)

class ExecutionResult(BaseModel):
    """Represents the result of an agent execution"""
    agent_id: str
    status: AgentState
    result: Any = None
    error: Optional[str] = None
    start_time: datetime
    end_time: datetime
    execution_time: float

class AgentExecutor:
    """Manages the execution of agents"""
    
    def __init__(self, max_concurrent: int = 10):
        self.max_concurrent = max_concurrent
        self._executor = ThreadPoolExecutor(max_workers=max_concurrent)
        self._running_agents: Dict[str, BaseAgent] = {}
        self._semaphore = asyncio.Semaphore(max_concurrent)

    async def execute_agent(self, agent: BaseAgent, input_data: Any) -> ExecutionResult:
        """Execute a single agent"""
        start_time = datetime.utcnow()
        
        try:
            async with self._semaphore:
                self._running_agents[agent.id] = agent
                await agent.initialize()
                
                result = await agent.execute(input_data)
                processed_result = await agent.process_response(result)
                
                end_time = datetime.utcnow()
                execution_time = (end_time - start_time).total_seconds()
                
                return ExecutionResult(
                    agent_id=agent.id,
                    status=AgentState.COMPLETED,
                    result=processed_result,
                    start_time=start_time,
                    end_time=end_time,
                    execution_time=execution_time
                )
        except Exception as e:
            logger.error(f"Error executing agent {agent.id}: {str(e)}")
            end_time = datetime.utcnow()
            execution_time = (end_time - start_time).total_seconds()
            
            return ExecutionResult(
                agent_id=agent.id,
                status=AgentState.ERROR,
                error=str(e),
                start_time=start_time,
                end_time=end_time,
                execution_time=execution_time
            )
        finally:
            await agent.cleanup()
            self._running_agents.pop(agent.id, None)

    async def execute_multiple(self, agents: List[BaseAgent], input_data: Any) -> List[ExecutionResult]:
        """Execute multiple agents concurrently"""
        tasks = [self.execute_agent(agent, input_data) for agent in agents]
        return await asyncio.gather(*tasks)

    def get_running_agents(self) -> Dict[str, BaseAgent]:
        """Get currently running agents"""
        return self._running_agents.copy()

    async def shutdown(self):
        """Shutdown the executor and cleanup resources"""
        for agent in list(self._running_agents.values()):
            await agent.cleanup()
        self._executor.shutdown(wait=True)
        self._running_agents.clear()