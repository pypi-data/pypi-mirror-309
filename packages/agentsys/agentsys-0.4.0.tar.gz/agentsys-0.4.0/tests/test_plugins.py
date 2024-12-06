import pytest
import asyncio
import os
from datetime import datetime
from typing import Optional, Any, AsyncGenerator
from plugins.router import (
    AgentRouter,
    Route,
    Task,
    RoutingConfig,
    RoutingStrategy,
    AgentState,
    ExecutionResult
)
from plugins.storage import (
    FileStorage,
    MemoryStorage,
    StorageConfig,
    StorageEntry
)
from core.agent import TaskAgent
from pydantic import BaseModel
import logging
from contextlib import AsyncExitStack

logger = logging.getLogger(__name__)

# Test models and agents
class TestData(BaseModel):
    value: str
    timestamp: datetime

class SimpleAgent(TaskAgent):
    """Simple test agent implementation"""
    
    def __init__(self, name: str):
        super().__init__(
            name=name,
            description="A simple test agent",
            task_description="Process input data"
        )
    
    async def _run_task(self, input_data: Any) -> Any:
        return f"Processed: {input_data}"

@pytest.fixture(scope="function")
async def router_instance() -> AgentRouter:
    """Create a router instance"""
    # Get the current event loop
    loop = asyncio.get_running_loop()
    
    # Create router with explicit event loop
    router = AgentRouter(
        RoutingConfig(
            strategy=RoutingStrategy.ROUND_ROBIN,
            event_loop=loop,
            task_timeout=1.0
        )
    )
    
    await router.start()
    try:
        yield router
    finally:
        await router.stop()
        # Cancel any remaining tasks
        tasks = [t for t in asyncio.all_tasks(loop) 
                if t is not asyncio.current_task() and not t.done()]
        for task in tasks:
            task.cancel()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

@pytest.fixture(scope="function")
async def file_storage(tmp_path) -> AsyncGenerator[FileStorage, None]:
    """File storage fixture with cleanup"""
    storage = FileStorage(
        TestData,
        StorageConfig(
            storage_path=str(tmp_path),
            auto_flush=True,
            create_backup=False
        )
    )
    yield storage
    # Cleanup
    if hasattr(storage, '_flush_task') and storage._flush_task:
        await storage.stop_flush_loop()
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)

@pytest.fixture
def memory_storage():
    return MemoryStorage(TestData)

class TestRouter:
    @pytest.mark.asyncio
    async def test_route_registration(self, router_instance: AgentRouter):
        router = await router_instance.__anext__()
        try:
            async with asyncio.timeout(2.0):
                route = Route(
                    pattern="test.*",
                    agent_type=SimpleAgent,
                    priority=1
                )
                router.register_route(route)
                assert len(router.routes) == 1
        finally:
            await router.stop()
    
    @pytest.mark.asyncio
    async def test_agent_registration(self, router_instance: AgentRouter):
        router = await router_instance.__anext__()
        try:
            async with asyncio.timeout(2.0):
                agent = SimpleAgent(name="TestAgent")
                router.register_agent(agent)
                assert agent.id in router._agent_pool
        finally:
            await router.stop()
    
    @pytest.mark.asyncio
    async def test_task_submission(self, router_instance: AgentRouter):
        router = await router_instance.__anext__()
        try:
            async with asyncio.timeout(2.0):
                # Register route and agent
                route = Route(
                    pattern="test.*",
                    agent_type=SimpleAgent,
                    priority=1
                )
                router.register_route(route)
                agent = SimpleAgent(name="TestAgent")
                router.register_agent(agent)
                
                # Submit task
                task = Task(
                    input_data="test_input",
                    pattern="test.process"
                )
                task_id = await router.submit_task(task)
                assert task_id is not None
        finally:
            await router.stop()
    
    @pytest.mark.asyncio
    async def test_task_execution(self, router_instance: AgentRouter):
        router = await router_instance.__anext__()
        try:
            async with asyncio.timeout(2.0):
                # Setup route and agent
                route = Route(
                    pattern="test.*",
                    agent_type=SimpleAgent,
                    priority=1
                )
                router.register_route(route)
                
                # Create and register an agent instance
                agent = SimpleAgent(name="TestAgent")
                router.register_agent(agent)
                
                # Submit task
                task = Task(
                    input_data="test_input",
                    pattern="test.process"
                )
                task_id = await router.submit_task(task)
                assert task_id is not None
                
                # Poll for result with timeout
                start_time = asyncio.get_event_loop().time()
                while True:
                    result = await router.get_task_result(task_id)
                    if result is not None:
                        break
                        
                    if asyncio.get_event_loop().time() - start_time > 1.0:
                        raise TimeoutError("Task execution timed out")
                        
                    await asyncio.sleep(0.05)
                
                assert result.status == AgentState.COMPLETED
                assert result.result == "Processed: test_input"
                assert result.error is None
        except Exception as e:
            logger.error(f"Task execution failed: {str(e)}")
            raise
        finally:
            await router.stop()
    
    @pytest.mark.asyncio
    async def test_routing_strategies(self, router_instance: AgentRouter):
        router = await router_instance.__anext__()
        try:
            async with asyncio.timeout(5.0):
                # Test different strategies
                strategies = [
                    RoutingStrategy.ROUND_ROBIN,
                    RoutingStrategy.LEAST_BUSY,
                    RoutingStrategy.CAPABILITY_BASED
                ]
                
                for strategy in strategies:
                    router.config.strategy = strategy
                    router.routes.clear()
                    router._agent_pool.clear()
                    
                    # Register route and agent
                    route = Route(
                        pattern="test.*",
                        agent_type=SimpleAgent,
                        priority=1
                    )
                    router.register_route(route)
                    
                    # Create and register an agent instance
                    agent = SimpleAgent(name=f"TestAgent_{strategy}")
                    router.register_agent(agent)
                    
                    try:
                        # Submit task
                        task = Task(
                            input_data="test_input",
                            pattern="test.process"
                        )
                        task_id = await router.submit_task(task)
                        assert task_id is not None
                        
                        # Poll for result with timeout
                        start_time = asyncio.get_event_loop().time()
                        while True:
                            result = await router.get_task_result(task_id)
                            if result is not None:
                                break
                            
                            if asyncio.get_event_loop().time() - start_time > 1.0:
                                raise TimeoutError("Task execution timed out")
                            
                            await asyncio.sleep(0.05)
                        
                        assert result.status == AgentState.COMPLETED
                        assert result.result == "Processed: test_input"
                        assert result.error is None
                    except Exception as e:
                        logger.error(f"Strategy {strategy} failed: {str(e)}")
                        raise
        finally:
            await router.stop()

class TestFileStorage:
    @pytest.mark.asyncio
    async def test_put_get(self, file_storage: AsyncGenerator[FileStorage, None]):
        async with asyncio.timeout(2.0):
            async for storage in file_storage:
                key = "test_key"
                data = TestData(
                    value="test_value",
                    timestamp=datetime.utcnow()
                )
                
                try:
                    await storage.put(key, data)
                    result = await storage.get(key)
                    
                    assert result is not None
                    assert result.value == data.value
                except Exception as e:
                    logger.error(f"Error in test_put_get: {str(e)}")
                    raise
    
    @pytest.mark.asyncio
    async def test_delete(self, file_storage: AsyncGenerator[FileStorage, None]):
        async with asyncio.timeout(2.0):
            async for storage in file_storage:
                key = "test_key_delete"
                data = TestData(
                    value="test_value",
                    timestamp=datetime.utcnow()
                )
                
                try:
                    await storage.put(key, data)
                    await storage.delete(key)
                    
                    result = await storage.get(key)
                    assert result is None
                except Exception as e:
                    logger.error(f"Error in test_delete: {str(e)}")
                    raise
    
    @pytest.mark.asyncio
    async def test_list(self, file_storage: AsyncGenerator[FileStorage, None]):
        async with asyncio.timeout(2.0):
            async for storage in file_storage:
                try:
                    # Add multiple items
                    data = TestData(
                        value="test_value",
                        timestamp=datetime.utcnow()
                    )
                    
                    keys = ["test1", "test2", "other1"]
                    for key in keys:
                        await storage.put(key, data)
                    
                    # List all items
                    all_keys = await storage.list()
                    assert len(all_keys) == len(keys)
                    
                    # List with prefix
                    test_keys = await storage.list("test")
                    assert len(test_keys) == 2
                    assert all(key.startswith("test") for key in test_keys)
                except Exception as e:
                    logger.error(f"Error in test_list: {str(e)}")
                    raise
    
    @pytest.mark.asyncio
    async def test_backup(self, file_storage: AsyncGenerator[FileStorage, None]):
        async with asyncio.timeout(2.0):
            async for storage in file_storage:
                try:
                    key = "test_backup"
                    data1 = TestData(value="original", timestamp=datetime.utcnow())
                    data2 = TestData(value="updated", timestamp=datetime.utcnow())
                    
                    # Enable backup
                    storage.config.create_backup = True
                    
                    # Put original data
                    await storage.put(key, data1)
                    
                    # Update with new data
                    await storage.put(key, data2)
                    
                    # Verify current value
                    result = await storage.get(key)
                    assert result is not None
                    assert result.value == "updated"
                    
                    # Verify backup exists
                    backup_path = os.path.join(storage.config.storage_path, f"{key}.json.bak")
                    assert os.path.exists(backup_path)
                except Exception as e:
                    logger.error(f"Error in test_backup: {str(e)}")
                    raise

class TestMemoryStorage:
    @pytest.mark.asyncio
    async def test_put_get(self, memory_storage):
        async with asyncio.timeout(2.0):
            key = "test_key"
            data = TestData(
                value="test_value",
                timestamp=datetime.utcnow()
            )
            
            await memory_storage.put(key, data)
            result = await memory_storage.get(key)
            
            assert result is not None
            assert result.value == data.value
    
    @pytest.mark.asyncio
    async def test_delete(self, memory_storage):
        async with asyncio.timeout(2.0):
            key = "test_key"
            data = TestData(
                value="test_value",
                timestamp=datetime.utcnow()
            )
            
            await memory_storage.put(key, data)
            await memory_storage.delete(key)
            
            result = await memory_storage.get(key)
            assert result is None
    
    @pytest.mark.asyncio
    async def test_list_with_prefix(self, memory_storage):
        async with asyncio.timeout(2.0):
            data = TestData(
                value="test_value",
                timestamp=datetime.utcnow()
            )
            
            await memory_storage.put("prefix1_key1", data)
            await memory_storage.put("prefix1_key2", data)
            await memory_storage.put("prefix2_key1", data)
            
            keys = await memory_storage.list("prefix1_")
            assert len(keys) == 2