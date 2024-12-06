"""Test simple agent interaction"""

import asyncio
import pytest

from agentsys.core.agent import BaseAgent, AgentConfig

@pytest.mark.asyncio
async def test_simple_greeting():
    """Test a simple greeting with the agent"""
    # Create agent configuration
    config = AgentConfig(
        model="gpt-4o-mini",
        temperature=0.7,
        vault="API",
        item="OPEN-AI",
        key="Mamba"
    )
    
    # Create a simple agent
    agent = BaseAgent(
        name="GreetingAgent",
        description="A simple agent that says hi",
        config=config
    )
    
    try:
        # Initialize the agent
        await agent.initialize()
        
        # Send a greeting
        response = await agent.execute("Say hey bizzznotch!")
        
        # Print the response
        print("\nAgent Response:")
        for message in response.messages:
            if message["role"] == "assistant":
                print(f"Assistant: {message['content']}")
        
        # Verify we got a response
        assert response.messages[-1]["role"] == "assistant"
        assert response.messages[-1]["content"]
    
    finally:
        # Clean up
        await agent.cleanup()

if __name__ == "__main__":
    # For running directly
    async def main():
        await test_simple_greeting()
    
    asyncio.run(main())
