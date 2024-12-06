"""
Simple example showing how to use the ChatAgent with memory capabilities.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from examples.chat import ChatAgent
import tempfile

# Create a temporary file for long-term memory storage
storage_path = os.path.join(tempfile.gettempdir(), "agent_memory.json")

# Create a chat agent with memory
agent = ChatAgent(
    name="Helper",
    description="A friendly AI assistant",
    instructions="You are a friendly and helpful AI assistant.",
    task_description="Engage in helpful conversations with users.",
    config={
        "memory_size": 100,  # Keep last 100 conversations in working memory
        "storage_path": storage_path  # Store conversations persistently
    }
)

# Have a simple conversation
response = agent.run([
    {"role": "user", "content": "Hi! What's your name?"}
])

print("Agent:", response["messages"][-1]["content"])

# Continue the conversation
response = agent.run([
    {"role": "user", "content": "Hi! What's your name?"},
    {"role": "assistant", "content": response["messages"][-1]["content"]},
    {"role": "user", "content": "Can you help me write a Python function to calculate fibonacci numbers?"}
])

print("\nAgent:", response["messages"][-1]["content"])

# The conversation is now stored in both working memory and long-term storage
# You can access it in future sessions using the same storage_path
