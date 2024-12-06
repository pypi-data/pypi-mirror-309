"""Interactive REPL for agents"""

import asyncio
from typing import Optional
from .core import Agent


async def _run_agent(agent: Agent, input_data: str) -> str:
    """Run the agent with the given input"""
    try:
        result = await agent.execute(input_data)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


def run_demo_loop(agent: Agent, prompt: str = "> ") -> None:
    """Run an interactive demo loop with the given agent"""
    print(f"\nStarting interactive session with {agent.name}")
    print("Type 'exit' or 'quit' to end the session\n")

    async def demo_loop():
        while True:
            try:
                user_input = input(prompt).strip()
                if user_input.lower() in ['exit', 'quit']:
                    break
                if not user_input:
                    continue
                
                result = await _run_agent(agent, user_input)
                print(result)
                print()  # Empty line for readability
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except EOFError:
                print("\nReceived EOF. Exiting...")
                break
            except Exception as e:
                print(f"Error: {str(e)}\n")
    
    try:
        # Run the async loop
        asyncio.run(demo_loop())
    except Exception as e:
        print(f"\nSession ended: {str(e)}")
    finally:
        print("\nSession ended. Goodbye!")
