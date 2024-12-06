import inspect
from datetime import datetime
from typing import get_origin, get_args, List, Dict, Any, Optional, Union


def debug_print(debug: bool, *args: str) -> None:
    if not debug:
        return
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = " ".join(map(str, args))
    print(f"\033[97m[\033[90m{timestamp}\033[97m]\033[90m {message}\033[0m")


def merge_fields(target, source):
    for key, value in source.items():
        if isinstance(value, str):
            target[key] += value
        elif value is not None and isinstance(value, dict):
            merge_fields(target[key], value)


def merge_chunk(final_response: dict, delta: dict) -> None:
    delta.pop("role", None)
    merge_fields(final_response, delta)

    tool_calls = delta.get("tool_calls")
    if tool_calls and len(tool_calls) > 0:
        index = tool_calls[0].pop("index")
        merge_fields(final_response["tool_calls"][index], tool_calls[0])


def get_type_info(annotation):
    """Get OpenAI-compatible type information from a type annotation."""
    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
        type(None): "null",
    }

    origin = get_origin(annotation)
    args = get_args(annotation)

    if origin is None:
        return {"type": type_map.get(annotation, "string")}
    
    if origin is list:
        return {"type": "array", "items": get_type_info(args[0])}
    elif origin is dict:
        return {"type": "object"}
    elif origin is Union:
        # Handle Optional[T] which is Union[T, None]
        if type(None) in args:
            non_none_type = next(arg for arg in args if arg is not type(None))
            return get_type_info(non_none_type)
    
    return {"type": "string"}


def function_to_json(func) -> dict:
    """
    Converts a Python function into a JSON-serializable dictionary
    that describes the function's signature, including its name,
    description, and parameters.

    Args:
        func: The function to be converted.

    Returns:
        A dictionary representing the function's signature in JSON format.
    """
    try:
        signature = inspect.signature(func)
    except ValueError as e:
        raise ValueError(
            f"Failed to get signature for function {func.__name__}: {str(e)}"
        )

    parameters = {}
    for param in signature.parameters.values():
        if param.name == "context_variables":
            continue
        parameters[param.name] = get_type_info(param.annotation)

    required = [
        param.name
        for param in signature.parameters.values()
        if param.default == inspect._empty and param.name != "context_variables"
    ]

    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": func.__doc__ or "",
            "parameters": {
                "type": "object",
                "properties": parameters,
                "required": required,
            },
        },
    }
