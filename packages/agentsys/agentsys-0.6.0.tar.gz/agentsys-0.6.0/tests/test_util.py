"""Tests for the util module."""

from typing import List, Dict, Any, Optional, Union
import pytest
from datetime import datetime
from swarm.util import (
    function_to_json,
    debug_print,
    merge_fields,
    merge_chunk,
    get_type_info,
)


def test_basic_function():
    def basic_function(arg1, arg2):
        return arg1 + arg2

    result = function_to_json(basic_function)
    assert result == {
        "type": "function",
        "function": {
            "name": "basic_function",
            "description": "",
            "parameters": {
                "type": "object",
                "properties": {
                    "arg1": {"type": "string"},
                    "arg2": {"type": "string"},
                },
                "required": ["arg1", "arg2"],
            },
        },
    }


def test_complex_function():
    def complex_function_with_types_and_descriptions(
        arg1: int, arg2: str, arg3: float = 3.14, arg4: bool = False
    ):
        """This is a complex function with a docstring."""
        pass

    result = function_to_json(complex_function_with_types_and_descriptions)
    assert result == {
        "type": "function",
        "function": {
            "name": "complex_function_with_types_and_descriptions",
            "description": "This is a complex function with a docstring.",
            "parameters": {
                "type": "object",
                "properties": {
                    "arg1": {"type": "integer"},
                    "arg2": {"type": "string"},
                    "arg3": {"type": "number"},
                    "arg4": {"type": "boolean"},
                },
                "required": ["arg1", "arg2"],
            },
        },
    }


def test_function_with_complex_types():
    """Test function with complex type hints."""
    def complex_types(
        arg1: List[str],
        arg2: Dict[str, Any],
        arg3: Optional[int] = None
    ) -> Dict[str, Any]:
        """Function with complex type hints."""
        pass

    result = function_to_json(complex_types)
    assert result["function"]["parameters"]["properties"]["arg1"]["type"] == "array"
    assert result["function"]["parameters"]["properties"]["arg2"]["type"] == "object"
    assert result["function"]["parameters"]["properties"]["arg3"]["type"] == "integer"


def test_function_with_docstring_args():
    """Test function with docstring argument descriptions."""
    def documented_function(arg1: str, arg2: int):
        """A function with documented arguments.
        
        Args:
            arg1: The first argument description
            arg2: The second argument description
        
        Returns:
            A string result
        """
        pass

    result = function_to_json(documented_function)
    assert "The first argument description" in result["function"]["description"]
    assert "The second argument description" in result["function"]["description"]


def test_function_with_context_variables():
    """Test function that uses context_variables parameter."""
    def with_context(context_variables: dict, arg1: str):
        """Function that uses context."""
        pass

    result = function_to_json(with_context)
    assert "context_variables" not in result["function"]["parameters"]["required"]
    assert "arg1" in result["function"]["parameters"]["required"]


def test_function_with_no_params():
    """Test function with no parameters."""
    def no_params():
        """Function with no parameters."""
        pass

    result = function_to_json(no_params)
    assert result["function"]["parameters"]["properties"] == {}


def test_debug_print(capsys):
    """Test debug print function."""
    # Test when debug is False
    debug_print(False, "test message")
    captured = capsys.readouterr()
    assert captured.out == ""

    # Test when debug is True
    debug_print(True, "test message")
    captured = capsys.readouterr()
    assert "test message" in captured.out
    assert datetime.now().strftime("%Y-%m-%d") in captured.out


def test_debug_print_formatting(capsys):
    """Test debug print timestamp formatting."""
    debug_print(True, "test message")
    captured = capsys.readouterr()
    
    # Check timestamp format
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    expected_prefix = f"[\033[90m{timestamp}\033[97m]"
    assert expected_prefix in captured.out
    
    # Check message formatting
    assert "\033[90m test message\033[0m" in captured.out


def test_merge_fields():
    """Test merge_fields function."""
    # Test merging strings
    target = {"content": "Hello ", "other": ""}
    source = {"content": "World", "other": "!"}
    merge_fields(target, source)
    assert target == {"content": "Hello World", "other": "!"}

    # Test merging nested dicts
    target = {"tool_calls": {"function": {"name": "test_", "args": ""}}}
    source = {"tool_calls": {"function": {"name": "func", "args": "{}"}}}
    merge_fields(target, source)
    assert target == {"tool_calls": {"function": {"name": "test_func", "args": "{}"}}}


def test_merge_fields_none_values():
    """Test merge_fields with None values at different levels."""
    # Test with None source
    target = {"content": "Hello"}
    merge_fields(target, None)
    assert target == {"content": "Hello"}
    
    # Test with nested None in source
    target = {"tool_calls": {"function": {"name": "test"}}}
    source = {"tool_calls": {"function": None}}
    merge_fields(target, source)
    assert target == {"tool_calls": {"function": {"name": "test"}}}


def test_merge_chunk():
    """Test merge_chunk function."""
    # Test merging content
    final_response = {"content": "Hello ", "tool_calls": [{"function": {"name": "", "arguments": ""}}]}
    delta = {"content": "World", "role": "assistant"}
    merge_chunk(final_response, delta)
    assert final_response["content"] == "Hello World"
    assert "role" not in final_response

    # Test merging tool calls
    final_response = {"content": "", "tool_calls": [{"function": {"name": "test_", "arguments": ""}}]}
    delta = {"tool_calls": [{"index": 0, "function": {"name": "func", "arguments": "{}"}}]}
    merge_chunk(final_response, delta)
    assert final_response["tool_calls"][0]["function"] == {"name": "test_func", "arguments": "{}"}


def test_merge_chunk_tool_calls():
    """Test merge_chunk with complex tool calls."""
    final_response = {
        "content": "",
        "tool_calls": [
            {"id": "1", "function": {"name": "test_", "arguments": ""}},
            {"id": "2", "function": {"name": "other_", "arguments": ""}}
        ]
    }
    delta = {
        "tool_calls": [
            {"index": 1, "function": {"name": "func", "arguments": "{}"}}
        ]
    }
    merge_chunk(final_response, delta)
    assert final_response["tool_calls"][1]["function"]["name"] == "other_func"


def test_get_type_info_edge_cases():
    """Test edge cases for get_type_info function."""
    # Test Union type
    assert get_type_info(Union[str, int]) == {"type": "string"}
    
    # Test Optional with non-string type
    assert get_type_info(Optional[int]) == {"type": "integer"}
    
    # Test nested List
    assert get_type_info(List[List[str]]) == {
        "type": "array",
        "items": {"type": "array", "items": {"type": "string"}}
    }
    
    # Test Dict with type args
    assert get_type_info(Dict[str, int]) == {"type": "object"}
    
    # Test unknown type
    class CustomType:
        pass
    assert get_type_info(CustomType) == {"type": "string"}


def test_get_type_info_complex_types():
    """Test get_type_info with complex type combinations."""
    # Test nested Optional types
    assert get_type_info(Optional[List[Optional[int]]]) == {
        "type": "array",
        "items": {"type": "integer"}
    }
    
    # Test multiple Union types
    assert get_type_info(Union[List[int], Dict[str, bool], None]) == {
        "type": "array",
        "items": {"type": "integer"}
    }
    
    # Test Dict with complex value type
    assert get_type_info(Dict[str, Union[int, float]]) == {"type": "object"}


def test_get_type_info_additional_cases():
    """Test additional cases for get_type_info."""
    # Test with None
    assert get_type_info(type(None)) == {"type": "null"}
    
    # Test with float
    assert get_type_info(float) == {"type": "number"}
    
    # Test with bool
    assert get_type_info(bool) == {"type": "boolean"}
    
    # Test with Union[str, int, None]
    assert get_type_info(Union[str, int, None]) == {"type": "string"}
    
    # Test with Dict[str, List[int]]
    assert get_type_info(Dict[str, List[int]]) == {"type": "object"}


def test_merge_fields_edge_cases():
    """Test merge_fields with edge cases."""
    # Test with None value
    target = {"content": "Hello"}
    source = {"content": None}
    merge_fields(target, source)
    assert target == {"content": "Hello"}

    # Test with nested None
    target = {"tool_calls": {"function": {"name": "test"}}}
    source = {"tool_calls": None}
    merge_fields(target, source)
    assert target == {"tool_calls": {"function": {"name": "test"}}}

    # Test with empty dict
    target = {"content": "Hello"}
    source = {}
    merge_fields(target, source)
    assert target == {"content": "Hello"}


def test_merge_chunk_edge_cases():
    """Test merge_chunk with edge cases."""
    # Test with missing tool_calls
    final_response = {"content": "Hello", "tool_calls": []}
    delta = {"content": " World"}
    merge_chunk(final_response, delta)
    assert final_response["content"] == "Hello World"
    assert final_response["tool_calls"] == []

    # Test with empty tool_calls
    final_response = {"content": "", "tool_calls": []}
    delta = {"tool_calls": []}
    merge_chunk(final_response, delta)
    assert final_response["tool_calls"] == []

    # Test with role field
    final_response = {"content": "", "tool_calls": []}
    delta = {"role": "assistant", "content": "Hello"}
    merge_chunk(final_response, delta)
    assert final_response["content"] == "Hello"
    assert "role" not in final_response


def test_function_to_json_complex():
    """Test function_to_json with complex function signatures."""
    def complex_func(
        arg1: Union[str, int],
        arg2: Optional[List[Dict[str, Any]]] = None,
        *args: str,
        **kwargs: int
    ) -> Dict[str, Any]:
        """A complex function with various parameter types."""
        pass

    result = function_to_json(complex_func)
    assert result["function"]["name"] == "complex_func"
    assert "arg1" in result["function"]["parameters"]["properties"]
    assert "arg2" in result["function"]["parameters"]["properties"]
    assert result["function"]["parameters"]["required"] == ["arg1"]
