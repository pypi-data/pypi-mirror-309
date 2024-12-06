import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import asyncio
from plugins.router import AgentRouter, RoutingConfig, RoutingStrategy, Task
from core.agent import BaseAgent as Agent, AgentState
from core.executor import ExecutionResult
from plugins.storage import FileStorage, StorageConfig

# 1. Define your agent
class AnalyticsAgent(Agent):
    def __init__(self, name: str, storage):
        super().__init__(name)
        self.storage = storage
    
    async def process(self, task: Task) -> ExecutionResult:
        try:
            # Process analytics
            result = await self._analyze(task.input)
            
            # Store results
            await self.storage.put(
                f"analytics_{task.id}",
                result
            )
            
            return ExecutionResult(
                status=AgentState.COMPLETED,
                result=result
            )
        except Exception as e:
            return ExecutionResult(
                status=AgentState.FAILED,
                error=str(e)
            )
    
    async def _analyze(self, data):
        # Your analytics logic here
        return {"analyzed": data}

# 2. Set up storage
storage = FileStorage(
    config=StorageConfig(
        base_path="./data",
        backup_enabled=True
    )
)

# 3. Configure and create router
router = AgentRouter(
    routing_config=RoutingConfig(
        strategy=RoutingStrategy.ROUND_ROBIN,
        timeout=60
    )
)

# 4. Create and register agent
analytics_agent = AnalyticsAgent("analytics_1", storage)

async def setup():
    await router.register_agent(analytics_agent)

# 5. Define routes
@router.route("analyze_data")
async def analyze_data(task: Task):
    return await analytics_agent.process(task)

# 6. Submit tasks
async def main():
    try:
        await setup()
        # Create task
        task = Task(
            input={"data": "sample"},
            metadata={"priority": "high"}
        )
        
        # Submit and wait for result
        result = await router.submit_task(task)
        
        # Check result
        if result.status == AgentState.COMPLETED:
            print(f"Analysis complete: {result.result}")
        else:
            print(f"Analysis failed: {result.error}")
    finally:
        # Clean up
        await router.stop()

# 7. Run the system
if __name__ == "__main__":
    asyncio.run(main())