"""
Tests for multi-agent interaction example.
"""

import pytest
from agentsys.core.agent import AgentConfig
from examples.agents.multi_agent import MathAgent, CalculatorAgent, FormatAgent

def create_agent_config(max_turns: int = 1) -> AgentConfig:
    """Helper function to create a consistent agent configuration"""
    return AgentConfig(
        model="gpt-4",
        temperature=0.7,
        max_tokens=None,
        stream=False,
        timeout=60.0,
        memory_size=1000,
        storage_path=None,
        max_turns=max_turns
    )

@pytest.mark.asyncio
async def test_calculator_agent():
    """Test calculator agent operations"""
    agent = CalculatorAgent(
        name="Calculator",
        description="Test calculator",
        task_description="Test calculations",
        config=create_agent_config()
    )
    
    # Test addition
    response = await agent.execute("add")
    assert "Addition result: 5" in response.messages[-1]["content"]
    
    # Test multiplication
    response = await agent.execute("multiply")
    assert "Multiplication result: 6" in response.messages[-1]["content"]

@pytest.mark.asyncio
async def test_format_agent():
    """Test format agent"""
    agent = FormatAgent(
        name="Formatter",
        description="Test formatter",
        task_description="Test formatting",
        config=create_agent_config()
    )
    
    response = await agent.execute("test result")
    assert "=== test result ===" in response.messages[-1]["content"]

@pytest.mark.asyncio
async def test_math_agent_flow():
    """Test complete math agent flow"""
    agent = MathAgent(
        name="MathBot",
        description="Test math operations",
        task_description="Test math queries",
        config=create_agent_config(max_turns=3)
    )
    
    # Test addition flow
    response = await agent.execute("add numbers")
    assert "Addition result" in response.messages[-1]["content"]
    
    # Test multiplication flow
    response = await agent.execute("multiply numbers")
    assert "Multiplication result" in response.messages[-1]["content"]
    
    # Verify context is maintained
    assert "operation" in response.context.variables

@pytest.mark.asyncio
async def test_agent_handoff():
    """Test agent handoff mechanism"""
    agent = MathAgent(
        name="MathBot",
        description="Test math operations",
        task_description="Test math queries",
        config=create_agent_config(max_turns=3)
    )
    
    # Get calculator agent
    calculator = await agent.calculate("test")
    assert isinstance(calculator, CalculatorAgent)
    
    # Get format agent
    formatter = await agent.format()
    assert isinstance(formatter, FormatAgent)
