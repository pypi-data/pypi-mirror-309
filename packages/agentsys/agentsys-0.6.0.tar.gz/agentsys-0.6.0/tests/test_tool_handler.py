"""Tests for the tool handler module."""

import pytest
from unittest.mock import Mock
import json

from swarm.orchestration.tool_handler import ToolHandler
from swarm.types import (
    Agent,
    ChatCompletionMessageToolCall,
    Function,
    Result,
)

class TestToolHandler:
    """Tests for the ToolHandler class."""

    def test_handle_function_result_with_result_object(self):
        """Test handling function result when a Result object is returned."""
        result = Result(value="test value", context_variables={"test": "value"})
        processed = ToolHandler.handle_function_result(result, debug=False)
        assert processed == result

    def test_handle_function_result_with_agent(self):
        """Test handling function result when an Agent is returned."""
        agent = Agent(name="Test Agent")
        processed = ToolHandler.handle_function_result(agent, debug=False)
        assert isinstance(processed, Result)
        assert json.loads(processed.value)["assistant"] == agent.name
        assert processed.agent == agent

    def test_handle_function_result_with_string(self):
        """Test handling function result when a string is returned."""
        processed = ToolHandler.handle_function_result("test string", debug=False)
        assert isinstance(processed, Result)
        assert processed.value == "test string"

    def test_handle_function_result_with_non_string(self):
        """Test handling function result when a non-string value is returned."""
        processed = ToolHandler.handle_function_result(123, debug=False)
        assert isinstance(processed, Result)
        assert processed.value == "123"

    def test_handle_function_result_with_error(self):
        """Test handle_function_result with a value that can't be converted to string."""
        class UnstringableObject:
            def __str__(self):
                raise ValueError("Can't convert to string")
        
        result = UnstringableObject()
        with pytest.raises(TypeError) as exc_info:
            ToolHandler.handle_function_result(result, debug=True)
        assert "Failed to cast response to string" in str(exc_info.value)

    def test_handle_tool_calls(self):
        """Test handling tool calls."""
        def test_function(arg1, arg2):
            return f"Received {arg1} and {arg2}"

        tool_calls = [
            ChatCompletionMessageToolCall(
                id="test_id",
                function=Function(
                    name="test_function",
                    arguments=json.dumps({"arg1": "value1", "arg2": "value2"})
                ),
                type="function"
            )
        ]

        response = ToolHandler.handle_tool_calls(
            tool_calls=tool_calls,
            functions=[test_function],
            context_variables={},
            debug=False
        )

        assert len(response.messages) == 1
        assert response.messages[0]["role"] == "tool"
        assert response.messages[0]["tool_call_id"] == "test_id"
        assert response.messages[0]["tool_name"] == "test_function"
        assert response.messages[0]["content"] == "Received value1 and value2"

    def test_handle_tool_calls_with_missing_function(self):
        """Test handling tool calls when the function is not found."""
        tool_calls = [
            ChatCompletionMessageToolCall(
                id="test_id",
                function=Function(
                    name="nonexistent_function",
                    arguments=json.dumps({"arg": "value"})
                ),
                type="function"
            )
        ]

        response = ToolHandler.handle_tool_calls(
            tool_calls=tool_calls,
            functions=[],
            context_variables={},
            debug=False
        )

        assert len(response.messages) == 1
        assert response.messages[0]["role"] == "tool"
        assert response.messages[0]["tool_call_id"] == "test_id"
        assert response.messages[0]["tool_name"] == "nonexistent_function"
        assert "Error: Tool nonexistent_function not found" in response.messages[0]["content"]

    def test_handle_tool_calls_with_context_variables(self):
        """Test handling tool calls with context variables."""
        def test_function(context_variables, arg):
            return f"Context: {context_variables['test']}, Arg: {arg}"

        tool_calls = [
            ChatCompletionMessageToolCall(
                id="test_id",
                function=Function(
                    name="test_function",
                    arguments=json.dumps({"arg": "value"})
                ),
                type="function"
            )
        ]

        response = ToolHandler.handle_tool_calls(
            tool_calls=tool_calls,
            functions=[test_function],
            context_variables={"test": "context_value"},
            debug=False
        )

        assert len(response.messages) == 1
        assert response.messages[0]["content"] == "Context: context_value, Arg: value"

    def test_handle_tool_calls_with_invalid_json(self):
        """Test handle_tool_calls with invalid JSON in arguments."""
        def test_func(arg1: str):
            return arg1

        tool_calls = [
            ChatCompletionMessageToolCall(
                id="1",
                function=Function(name="test_func", arguments="{invalid json}"),
            )
        ]
        functions = [test_func]
        
        with pytest.raises(json.JSONDecodeError):
            ToolHandler.handle_tool_calls(tool_calls, functions, {}, debug=True)

    def test_handle_tool_calls_with_debug(self):
        """Test handle_tool_calls with debug enabled."""
        def test_func(arg1: str):
            return f"Hello {arg1}"

        tool_calls = [
            ChatCompletionMessageToolCall(
                id="1",
                function=Function(name="test_func", arguments='{"arg1": "World"}'),
            )
        ]
        functions = [test_func]
        
        response = ToolHandler.handle_tool_calls(tool_calls, functions, {}, debug=True)
        assert len(response.messages) == 1
        assert response.messages[0]["content"] == "Hello World"

    def test_handle_tool_calls_with_missing_tool(self):
        """Test handle_tool_calls with a missing tool."""
        def test_func(arg1: str):
            return arg1

        tool_calls = [
            ChatCompletionMessageToolCall(
                id="1",
                function=Function(name="non_existent_tool", arguments='{"arg1": "test"}'),
            )
        ]
        functions = [test_func]
        
        response = ToolHandler.handle_tool_calls(tool_calls, functions, {}, debug=True)
        assert len(response.messages) == 1
        assert "Error: Tool non_existent_tool not found" in response.messages[0]["content"]

    def test_handle_tool_calls_with_context_variables(self):
        """Test handle_tool_calls with context variables."""
        def test_func_with_context(context_variables: dict, arg1: str):
            return f"Context: {context_variables.get('test_key')}, Arg: {arg1}"

        tool_calls = [
            ChatCompletionMessageToolCall(
                id="1",
                function=Function(name="test_func_with_context", arguments='{"arg1": "test"}'),
            )
        ]
        functions = [test_func_with_context]
        context = {"test_key": "test_value"}
        
        response = ToolHandler.handle_tool_calls(tool_calls, functions, context, debug=True)
        assert len(response.messages) == 1
        assert "Context: test_value, Arg: test" in response.messages[0]["content"]

    def test_handle_tool_calls_with_error(self):
        """Test handle_tool_calls with a function that raises an error."""
        def error_func(arg1: str):
            raise ValueError("Test error")

        tool_calls = [
            ChatCompletionMessageToolCall(
                id="1",
                function=Function(name="error_func", arguments='{"arg1": "test"}'),
            )
        ]
        functions = [error_func]
        
        with pytest.raises(ValueError, match="Test error"):
            ToolHandler.handle_tool_calls(tool_calls, functions, {}, debug=True)
