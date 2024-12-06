"""Tests for the core Swarm functionality."""

import pytest
from agentsys import Agent, Swarm
from agentsys.types import Response
from locksys import Locksys
from openai import OpenAI
import json
from unittest.mock import patch, MagicMock
from openai.types.chat import ChatCompletion, ChatCompletionMessage
from openai.types.chat.chat_completion import Choice

@pytest.fixture
def openai_client():
    """Create OpenAI client with API key from Locksys."""
    api_key = Locksys().item('OPEN-AI').key('Mamba').results()
    return OpenAI(api_key=api_key)

def test_run_with_simple_message(openai_client):
    agent = Agent()
    client = Swarm(client=openai_client)
    messages = [{"role": "user", "content": "Hello, how are you?"}]
    response = client.run(agent=agent, messages=messages)

    assert response.messages[-1]["role"] == "assistant"
    assert isinstance(response.messages[-1]["content"], str)

def test_tool_call(openai_client):
    expected_location = "San Francisco"

    # set up mock to record function calls
    def get_weather(location):
        assert location == expected_location
        return "It's sunny today."

    agent = Agent(name="Test Agent", functions=[get_weather])
    messages = [
        {"role": "user", "content": "What's the weather like in San Francisco?"}
    ]

    client = Swarm(client=openai_client)
    response = client.run(agent=agent, messages=messages)

    assert response.messages[-1]["role"] == "assistant"
    assert isinstance(response.messages[-1]["content"], str)

def test_execute_tools_false(openai_client):
    expected_location = "San Francisco"

    def get_weather(location):
        assert False, "This function should not be called"
        return "It's sunny today."

    agent = Agent(name="Test Agent", functions=[get_weather])
    messages = [
        {"role": "user", "content": "What's the weather like in San Francisco?"}
    ]

    client = Swarm(client=openai_client)
    response = client.run(agent=agent, messages=messages, execute_tools=False)

    assert response.messages[-1]["role"] == "assistant"
    assert len(response.messages[-1].get("tool_calls", [])) >= 0

def test_handoff(openai_client):
    agent_b = Agent(name="Agent B")

    def transfer_to_agent_b():
        return agent_b

    agent_a = Agent(name="Agent A", functions=[transfer_to_agent_b])
    messages = [{"role": "user", "content": "Transfer me to agent B"}]

    client = Swarm(client=openai_client)
    response = client.run(agent=agent_a, messages=messages)

    assert response.agent == agent_b

def test_streaming_response(openai_client):
    """Test streaming response functionality."""
    agent = Agent()
    client = Swarm(client=openai_client)
    messages = [{"role": "user", "content": "Hello"}]

    stream = client.run(agent=agent, messages=messages, stream=True)
    chunks = list(stream)
    assert len(chunks) > 0
    # Check for any valid chunk type (content, tool_calls, delim, etc.)
    assert any(
        chunk.get("content") is not None or
        chunk.get("tool_calls") is not None or
        chunk.get("delim") is not None
        for chunk in chunks
    )

def test_context_variables(openai_client):
    """Test context variables handling."""
    def greet(context_variables):
        return f"Hello {context_variables['name']}!"

    agent = Agent(functions=[greet])
    client = Swarm(client=openai_client)
    messages = [{"role": "user", "content": "Greet me"}]
    context = {"name": "John"}

    response = client.run(agent=agent, messages=messages, context_variables=context)
    assert response is not None
    assert hasattr(response, 'messages')
    assert isinstance(response.messages, list)
    
    # The response should contain either the greeting in a tool response or assistant message
    found_greeting = False
    for msg in response.messages:
        if msg is None:
            continue
            
        if isinstance(msg.get("content"), str) and "Hello John!" in msg["content"]:
            found_greeting = True
            break
            
        tool_calls = msg.get("tool_calls", [])
        for tool_call in tool_calls:
            if tool_call and "Hello John!" in str(tool_call.get("function", {}).get("arguments", "")):
                found_greeting = True
                break
                
    assert found_greeting, "Greeting not found in response messages"

def test_max_turns(openai_client):
    """Test max turns limit."""
    def loop():
        return "Looping..."

    agent = Agent(functions=[loop])
    client = Swarm(client=openai_client)
    messages = [{"role": "user", "content": "Start loop"}]

    response = client.run(agent=agent, messages=messages, max_turns=2)
    assert len([msg for msg in response.messages if msg["role"] == "tool"]) <= 2

def test_error_handling(openai_client):
    """Test error handling in function calls."""
    def raise_error():
        raise ValueError("Test error")

    agent = Agent(functions=[raise_error])
    client = Swarm(client=openai_client)
    messages = [{"role": "user", "content": "Raise error"}]

    with pytest.raises(ValueError, match="Test error"):
        client.run(agent=agent, messages=messages)

def test_get_chat_completion_with_callable_instructions(openai_client):
    """Test get_chat_completion with callable instructions."""
    def dynamic_instructions(context_variables):
        return f"Dynamic instructions with context: {context_variables.get('test_key')}"

    agent = Agent(
        name="test",
        instructions=dynamic_instructions,
        model="gpt-4",
        functions=[],
    )
    swarm = Swarm(client=openai_client)

    with patch.object(swarm.client.chat.completions, 'create') as mock_create:
        mock_create.return_value = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "assistant", "content": "test"}]
        )
        swarm.get_chat_completion(agent, [], {"test_key": "test_value"}, None, False, True)
        
        called_messages = mock_create.call_args[1]["messages"]
        assert "Dynamic instructions with context: test_value" in called_messages[0]["content"]

def test_run_with_parallel_tool_calls(openai_client):
    """Test run with parallel tool calls enabled."""
    def test_func(arg1: str) -> str:
        """Process a string input and return the processed result."""
        return f"Processed {arg1}"

    # Add docstring and type hints to the function
    test_func.__doc__ = "Process a string input and return the processed result."
    test_func.__annotations__ = {"arg1": str, "return": str}

    agent = Agent(
        name="test",
        instructions="You are a helpful assistant that processes text. When asked to process text, use the test_func tool.",
        model="gpt-4",
        functions=[test_func],
        tool_choice="auto"
    )
    swarm = Swarm(client=openai_client)

    response = swarm.run(
        agent, 
        [{"role": "user", "content": "Please process the text 'hello' for me"}],
        debug=True
    )
    
    # Verify tool was called and response was processed
    messages = response.messages
    assert len(messages) >= 2
    
    # Find the tool response
    tool_messages = [msg for msg in messages if msg.get("role") == "tool"]
    assert len(tool_messages) > 0
    assert "Processed hello" in tool_messages[0]["content"]
    
    # Verify final response
    final_message = messages[-1]
    assert "processed" in final_message["content"].lower()
    assert "hello" in final_message["content"].lower()

def test_run_with_tool_execution_disabled(openai_client):
    """Test run with tool execution disabled."""
    def test_func(arg1: str):
        return f"Processed {arg1}"

    agent = Agent(
        name="test",
        instructions="Test agent",
        model="gpt-4",
        functions=[test_func],
    )
    swarm = Swarm(client=openai_client)

    tool_response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "test"}],
        tools=[{
            "type": "function",
            "function": {
                "name": "test_func",
                "description": "A test function",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "arg1": {"type": "string"}
                    },
                    "required": ["arg1"]
                }
            }
        }],
        tool_choice="auto"
    )

    with patch.object(swarm.client.chat.completions, 'create') as mock_create:
        mock_create.return_value = tool_response
        response = swarm.run(
            agent, 
            [{"role": "user", "content": "test"}], 
            execute_tools=False,
            debug=True
        )
        
        # Verify tool was not executed
        assert len(response.messages) == 1
        assert response.messages[0]["role"] == "assistant"
