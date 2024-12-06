import pytest
import asyncio
from datetime import datetime
from typing import Any
from core.agent import TaskAgent, AgentState, AgentConfig

class SimpleAgent(TaskAgent):
    """A simple test agent"""
    def __init__(self, name: str = "TestAgent"):
        super().__init__(
            name=name,
            description="A simple test agent for testing",
            task_description="Execute simple test tasks"
        )
        
    async def execute(self, input_data: Any) -> Any:
        self.state = AgentState.RUNNING
        result = f"Processed: {input_data}"
        self.state = AgentState.COMPLETED
        return result

@pytest.fixture
async def simple_agent():
    agent = SimpleAgent()
    await agent.initialize()
    try:
        yield agent
    finally:
        await agent.cleanup()

class TestBaseAgent:
    @pytest.mark.asyncio
    async def test_agent_initialization(self):
        agent = TaskAgent(
            name="TestAgent",
            description="Test agent",
            task_description="Test tasks"
        )
        assert agent.state == AgentState.IDLE
        assert agent.name == "TestAgent"
    
    @pytest.mark.asyncio
    async def test_agent_context_management(self):
        agent = TaskAgent(
            name="TestAgent",
            description="Test agent",
            task_description="Test tasks"
        )
        agent.context.variables["key"] = "value"
        assert agent.context.variables["key"] == "value"
    
    @pytest.mark.asyncio
    async def test_agent_execution(self):
        agent = TaskAgent(
            name="TestAgent",
            description="Test agent",
            task_description="Test tasks"
        )
        with pytest.raises(NotImplementedError):
            await agent.execute("test")
    
    @pytest.mark.asyncio
    async def test_agent_config(self):
        custom_config = AgentConfig(
            model="gpt-3.5-turbo",
            temperature=0.5,
            max_tokens=100
        )
        agent = TaskAgent(
            name="TestAgent",
            description="Test agent",
            task_description="Test tasks",
            config=custom_config
        )
        assert agent.config.model == "gpt-3.5-turbo"
        assert agent.config.temperature == 0.5
        assert agent.config.max_tokens == 100

class TestSimpleAgent:
    @pytest.mark.asyncio
    async def test_agent_initialization(self, simple_agent):
        agent = await anext(simple_agent)
        assert agent.name == "TestAgent"
        assert agent.state == AgentState.IDLE
    
    @pytest.mark.asyncio
    async def test_agent_execution(self, simple_agent):
        agent = await anext(simple_agent)
        result = await agent.execute("test_input")
        assert result == "Processed: test_input"
    
    @pytest.mark.asyncio
    async def test_agent_context(self, simple_agent):
        agent = await anext(simple_agent)
        # Test context management
        agent.context.variables["key"] = "value"
        assert agent.context.variables["key"] == "value"
        
        # Test context clearing
        agent.context.variables.clear()
        assert "key" not in agent.context.variables
    
    @pytest.mark.asyncio
    async def test_agent_state_transitions(self, simple_agent):
        agent = await anext(simple_agent)
        assert agent.state == AgentState.IDLE
        
        # State should change during execution
        execution = agent.execute("test_input")
        assert agent.state == AgentState.IDLE
        
        result = await execution
        assert result == "Processed: test_input"
        assert agent.state == AgentState.COMPLETED
    
    @pytest.mark.asyncio
    async def test_agent_metadata(self, simple_agent):
        agent = await anext(simple_agent)
        
        # Test metadata in context
        agent.context.metadata["session_id"] = "test-123"
        agent.context.metadata["user"] = "test-user"
        
        assert agent.context.metadata["session_id"] == "test-123"
        assert agent.context.metadata["user"] == "test-user"
        
        # Test metadata clearing
        agent.context.metadata.clear()
        assert len(agent.context.metadata) == 0