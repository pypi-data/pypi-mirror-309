"""
Interactive chat REPL using the ChatAgent.
"""

from agentsys.core import ChatAgent
import tempfile
import os

def run_chat_session(agent: ChatAgent):
    """Run an interactive chat session with the agent."""
    print(f"\nStarting chat with {agent.name}")
    print("Type 'exit' or 'quit' to end the session\n")
    
    conversation = []
    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ['exit', 'quit']:
                break
            
            # Add user message and get response
            conversation.append({"role": "user", "content": user_input})
            response = agent.run(conversation)
            
            # Update conversation with assistant's response
            conversation = response["messages"]
            print("\nAgent:", response["messages"][-1]["content"], "\n")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {str(e)}")
            break
    
    print("\nChat session ended")

if __name__ == "__main__":
    # Create a temporary file for long-term memory storage
    storage_path = os.path.join(tempfile.gettempdir(), "chat_memory.json")
    
    # Create the agent
    agent = ChatAgent(
        name="ChatBot",
        description="An interactive chat bot",
        instructions="You are a friendly and knowledgeable AI assistant. Be concise but helpful.",
        task_description="Engage in interactive chat sessions with users.",
        config={
            "memory_size": 1000,  # Keep last 1000 conversations in working memory
            "storage_path": storage_path  # Store conversations persistently
        }
    )
    
    # Start the chat session
    run_chat_session(agent)
