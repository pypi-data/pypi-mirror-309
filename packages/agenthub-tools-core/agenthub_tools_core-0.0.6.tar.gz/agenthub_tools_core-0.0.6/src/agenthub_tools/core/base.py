# core/src/agenthub_tools/core/base.py
from typing import Callable, Dict
from functools import wraps
import inspect

def tool(description: str) -> Callable:
    """
    Decorator to mark a function as an agent tool.
    
    Args:
        description: Description of what the tool does
        
    Returns:
        Decorated function with metadata
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> str:
            result = func(*args, **kwargs)
            if not isinstance(result, str):
                raise TypeError(f"Tool must return string, got {type(result)}")
            return result
            
        # Store metadata about the tool
        wrapper.is_tool = True
        wrapper.description = description
        wrapper.parameters = {
            name: {
                "type": "string" if param.annotation == str else "number",
                "description": "",  # Could be added via docstring parsing
                "required": param.default == inspect.Parameter.empty
            }
            for name, param in inspect.signature(func).parameters.items()
        }
        
        return wrapper
    return decorator

def get_tool_spec(func: Callable) -> Dict:
    """Convert a tool function to OpenAI function specification format."""
    if not hasattr(func, 'is_tool'):
        raise ValueError("Function is not marked as a tool")
        
    return {
        "name": func.__name__,
        "description": func.description,
        "parameters": {
            "type": "object",
            "properties": func.parameters,
            "required": [
                name for name, param in func.parameters.items()
                if param["required"]
            ]
        }
    }