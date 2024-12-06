"""Tests for the REPL module."""

import pytest
from unittest.mock import Mock, patch
from swarm.repl.repl import (
    run_demo_loop,
    process_and_print_streaming_response,
    pretty_print_messages,
)
from swarm import Swarm, Agent, Response
from locksys import Locksys
from openai import OpenAI

@pytest.fixture
def openai_client():
    """Create OpenAI client with API key from Locksys."""
    api_key = Locksys().item('OPEN-AI').key('Mamba').results()
    return OpenAI(api_key=api_key)

class TestRepl:
    """Tests for the REPL module."""

    @pytest.fixture
    def mock_input(self):
        with patch('builtins.input') as mock:
            yield mock

    @pytest.fixture
    def mock_print(self):
        with patch('builtins.print') as mock:
            yield mock

    def test_pretty_print_messages(self, mock_print):
        """Test message pretty printing."""
        messages = [
            {"role": "user", "content": "Hello"},
            {
                "role": "assistant",
                "sender": "TestAgent",
                "content": "Hi there!",
                "tool_calls": [
                    {
                        "function": {
                            "name": "test_tool",
                            "arguments": '{"arg": "value"}'
                        }
                    }
                ]
            }
        ]
        pretty_print_messages(messages)
        assert mock_print.call_count >= 2  # Agent name + content + tool call

    def test_process_streaming_response(self, mock_print):
        """Test streaming response processing."""
        events = [
            {"sender": "TestAgent", "content": "Hello"},
            {"content": " World"},
            {
                "tool_calls": [{
                    "function": {
                        "name": "test",
                        "arguments": "{}"
                    }
                }]
            },
            {"delim": "end"},
            {"messages": []}  
        ]
        
        result = process_and_print_streaming_response(events)
        assert mock_print.call_count >= len(events)
        assert isinstance(result, Response)
        assert result.messages == []
        assert result.agent is None
        assert result.context_variables == {}

    def test_run_demo_loop(self, mock_input, mock_print, openai_client):
        """Test the demo loop."""
        mock_input.side_effect = ["Hello", KeyboardInterrupt()]
        agent = Agent(name="Test Agent")
        
        # Create a list to store streamed chunks
        chunks = [
            {"content": "Hi"},
            {"content": " there"},
            {"delim": "end"},
            {"messages": [{"role": "assistant", "content": "Hi there"}]}  
        ]

        # Mock the Swarm.run method to return our chunks
        with patch('swarm.repl.repl.Swarm') as mock_swarm_class:
            mock_swarm = Mock()
            mock_swarm.run.return_value = iter(chunks)  # Return an iterator of chunks
            mock_swarm_class.return_value = mock_swarm
            
            run_demo_loop(agent, stream=True)
            
            # Should have printed welcome message
            assert any("Starting Swarm CLI" in str(call) for call in mock_print.call_args_list)
            # Should have processed one message before exit
            assert mock_swarm.run.call_count == 1
