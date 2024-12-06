"""
Example showing how to use function calls with the simplified AgentSys interface.
"""

from agentsys.simple import AgentSys, Agent

def greet(context_variables, language):
    """Greet the user in the specified language."""
    user_name = context_variables["user_name"]
    greeting = "Hola" if language.lower() == "spanish" else "Hello"
    print(f"{greeting}, {user_name}!")
    return "Done"

# Create a client
client = AgentSys()

# Create an agent with the greet function
agent = Agent(
    name="GreetingAgent",
    instructions="You are a helpful agent that can greet users in different languages. Use the greet() function when asked.",
    functions=[greet]
)

# Run with Spanish greeting
response = client.run(
    agent=agent,
    messages=[{"role": "user", "content": "Usa greet() por favor."}],
    context_variables={"user_name": "John"}
)
print("\nResponse:", response["messages"][-1]["content"])

# Run with English greeting
response = client.run(
    agent=agent,
    messages=[{"role": "user", "content": "Use greet() in English please."}],
    context_variables={"user_name": "Maria"}
)
print("\nResponse:", response["messages"][-1]["content"])

# You can also use the convenience function:
from agentsys.simple import run

response = run(
    agent=agent,
    messages=[{"role": "user", "content": "Greet me in Spanish!"}],
    context_variables={"user_name": "Alice"}
)
print("\nResponse:", response["messages"][-1]["content"])
