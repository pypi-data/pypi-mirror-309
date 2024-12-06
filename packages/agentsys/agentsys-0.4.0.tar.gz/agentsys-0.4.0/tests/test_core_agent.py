"""Tests for core agent functionality."""

import pytest
from datetime import datetime
from agentsys.core import (
    BaseAgent,
    AgentConfig,
    AgentState,
    AgentContext,
    AgentResponse,
    ToolCall,
    WorkingMemory,
    MemoryManager
)

class SimpleTestAgent(BaseAgent):
    """Simple agent implementation for testing"""
    async def _run_turn(self, input_data, messages):
        """Simple implementation that echoes input"""
        response = {
            "messages": messages + [{"role": "assistant", "content": f"Processed: {input_data}"}],
            "agent": self,
            "context": self.context,
            "tool_calls": []
        }
        return AgentResponse(**response)

async def mock_tool(x: int) -> int:
    """Mock tool that doubles its input"""
    return x * 2

@pytest.mark.asyncio
async def test_agent_initialization():
    """Test agent initialization and configuration"""
    config = AgentConfig(model="test-model", temperature=0.5, max_turns=5)
    agent = SimpleTestAgent(
        name="TestAgent",
        description="Test agent description",
        config=config
    )
    
    # Check basic properties
    assert agent.name == "TestAgent"
    assert agent.description == "Test agent description"
    assert agent.state == AgentState.IDLE
    assert isinstance(agent.id, str)
    assert isinstance(agent.created_at, datetime)
    
    # Check configuration
    assert agent.config.model == "test-model"
    assert agent.config.temperature == 0.5
    assert agent.config.max_turns == 5
    
    # Check memory initialization
    assert isinstance(agent.memory, MemoryManager)
    assert isinstance(agent.memory.working_memory, WorkingMemory)
    assert agent.memory.working_memory.max_size == agent.config.memory_size

@pytest.mark.asyncio
async def test_agent_execution():
    """Test basic agent execution flow"""
    agent = SimpleTestAgent(
        name="TestAgent",
        description="Test agent description",
        config=AgentConfig(max_turns=3)
    )
    
    # Test single turn execution
    response = await agent.execute("test input")
    assert agent.state == AgentState.COMPLETED
    assert len(response.messages) == 1
    assert "Processed: test input" in response.messages[0]["content"]
    
    # Verify context persistence
    assert isinstance(response.context, AgentContext)
    assert response.context == agent.context

@pytest.mark.asyncio
async def test_agent_tool_execution():
    """Test agent tool execution"""
    agent = SimpleTestAgent(
        name="TestAgent",
        description="Test agent description",
        config=AgentConfig(max_turns=3, execute_tools=True)
    )
    
    # Add a mock tool
    agent.tools = [mock_tool]
    
    # Create a response with a tool call
    tool_call = ToolCall(name="mock_tool", arguments={"x": 5})
    response = await agent.execute("test with tool")
    
    # Verify tool execution
    assert response.tool_calls == []  # Our simple agent doesn't make tool calls
    assert agent.state == AgentState.COMPLETED

@pytest.mark.asyncio
async def test_agent_memory():
    """Test agent memory management"""
    agent = SimpleTestAgent(
        name="TestAgent",
        description="Test agent description",
        config=AgentConfig(memory_size=5)
    )
    
    # Test memory operations
    agent.memory.working_memory.add("test_key", "test_value")
    assert agent.memory.working_memory.get("test_key") == "test_value"
    
    # Test memory size limit
    for i in range(10):
        agent.memory.working_memory.add(f"key_{i}", f"value_{i}")
    
    assert len(agent.memory.working_memory.items) <= 5

@pytest.mark.asyncio
async def test_agent_error_handling():
    """Test agent error handling"""
    class ErrorAgent(SimpleTestAgent):
        async def _run_turn(self, input_data, messages):
            raise Exception("Test error")
    
    agent = ErrorAgent(
        name="ErrorAgent",
        description="Test error handling"
    )
    
    # Test error state
    with pytest.raises(Exception):
        await agent.execute("test input")
    assert agent.state == AgentState.ERROR
