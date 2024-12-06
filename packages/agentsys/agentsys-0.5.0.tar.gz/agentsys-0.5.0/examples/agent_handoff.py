"""
Example showing how to use agent handoffs with AgentSys.
"""

from agentsys.core import Agent, run

# Create specialized agents
sales_agent = Agent(
    name="Sales Agent",
    instructions="You are a helpful sales agent. Help customers with their purchases."
)

support_agent = Agent(
    name="Support Agent",
    instructions="You are a helpful support agent. Help customers with technical issues."
)

# Create transfer functions
def transfer_to_sales():
    """Transfer the conversation to the sales agent."""
    return sales_agent

def transfer_to_support():
    """Transfer the conversation to the support agent."""
    return support_agent

# Create the main agent with transfer capabilities
main_agent = Agent(
    name="Main Agent",
    instructions="You are a helpful agent that can transfer customers to sales or support.",
    functions=[transfer_to_sales, transfer_to_support]
)

# Run with transfer to sales
response = main_agent.run([
    {"role": "user", "content": "I want to buy something."}
])
print(f"\nAgent: {response.agent.name}")
print(f"Response: {response.messages[-1]['content']}")

# Continue with the new agent
if response.agent != main_agent:
    response = response.agent.run([
        {"role": "user", "content": "Tell me about your products."}
    ])
    print(f"\nAgent: {response.agent.name}")
    print(f"Response: {response.messages[-1]['content']}")

# Try transfer to support
response = main_agent.run([
    {"role": "user", "content": "I need help with a technical issue."}
])
print(f"\nAgent: {response.agent.name}")
print(f"Response: {response.messages[-1]['content']}")

# Continue with the new agent
if response.agent != main_agent:
    response = response.agent.run([
        {"role": "user", "content": "My device isn't working."}
    ])
    print(f"\nAgent: {response.agent.name}")
    print(f"Response: {response.messages[-1]['content']}")

# You can also use the convenience function:
response = run(main_agent, [
    {"role": "user", "content": "Can you help me with a purchase?"}
])
