from agentsys.core import Agent
import json


def add_numbers(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b


def subtract_numbers(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b


def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b


def divide_numbers(a: float, b: float) -> float:
    """Divide a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


# Create a calculator agent
calculator_agent = Agent(
    name="Calculator Agent",
    instructions="""A helpful calculator that can perform basic arithmetic operations.
    When users ask you to perform calculations, use the appropriate function.
    For addition, use add_numbers
    For subtraction, use subtract_numbers
    For multiplication, use multiply_numbers
    For division, use divide_numbers
    
    Always show your work and explain the calculation steps to the user.
    """,
    functions=[add_numbers, subtract_numbers, multiply_numbers, divide_numbers]
)


if __name__ == "__main__":
    from agentsys.repl import run_demo_loop
    
    # Start the interactive loop
    run_demo_loop(calculator_agent)
