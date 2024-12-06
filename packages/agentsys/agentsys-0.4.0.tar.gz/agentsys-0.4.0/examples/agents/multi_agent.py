"""
Example demonstrating multi-agent interaction with tools and context.
"""

import asyncio
from typing import Any
from agentsys.core import TaskAgent, AgentConfig, AgentContext

class CalculatorAgent(TaskAgent):
    """Agent that performs calculations"""
    
    async def add(self, a: float, b: float) -> float:
        """Add two numbers"""
        return a + b
    
    async def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers"""
        return a * b
    
    async def _run_task(self, input_data: str) -> Any:
        self.tools = [self.add, self.multiply]
        
        if "multiply" in input_data.lower():
            result = await self.multiply(2, 3)
            return f"Multiplication result: {result}"
        else:
            result = await self.add(2, 3)
            return f"Addition result: {result}"

class FormatAgent(TaskAgent):
    """Agent that formats results"""
    
    async def format_result(self, result: str) -> str:
        """Format the calculation result"""
        return f"=== {result} ==="
    
    async def _run_task(self, input_data: str) -> Any:
        self.tools = [self.format_result]
        return await self.format_result(input_data)

class MathAgent(TaskAgent):
    """Main agent that coordinates calculations"""
    
    async def calculate(self, operation: str) -> TaskAgent:
        """Perform calculation and hand off to formatter"""
        calculator = CalculatorAgent(
            name="Calculator",
            description="Perform calculations",
            task_description="Calculate results",
            config=AgentConfig(max_turns=2)
        )
        
        # Store operation in context for later
        self.update_context(operation=operation)
        return calculator
    
    async def format(self) -> TaskAgent:
        """Hand off to format agent"""
        return FormatAgent(
            name="Formatter",
            description="Format results",
            task_description="Format calculation results",
            config=AgentConfig(max_turns=1)
        )
    
    async def _run_task(self, input_data: str) -> Any:
        self.tools = [self.calculate, self.format]
        
        # First, calculate
        calculator = await self.calculate(input_data)
        result = await calculator.execute(input_data)
        
        # Then format
        formatter = await self.format()
        formatted_result = await formatter.execute(result.messages[-1]["content"])
        
        return formatted_result.messages[-1]["content"]

async def main():
    # Create the main agent
    agent = MathAgent(
        name="MathBot",
        description="Handle math operations",
        task_description="Process math queries",
        config=AgentConfig(max_turns=3)
    )
    
    # Test addition
    print("\nTesting addition:")
    response = await agent.execute("add numbers")
    print(response.messages[-1]["content"])
    
    # Test multiplication
    print("\nTesting multiplication:")
    response = await agent.execute("multiply numbers")
    print(response.messages[-1]["content"])

if __name__ == "__main__":
    asyncio.run(main())
