from typing import Any, Dict, List
from core.agent import TaskAgent
from middleware.cache import cache_response
from middleware.retry import with_retry
from middleware.telemetry import with_telemetry
from protocols.messaging import MessageBus, MessageType, Message
import asyncio
import json

class ChatbotAgent(TaskAgent):
    """An example chatbot agent that can engage in conversations"""
    
    def __init__(self, name: str = "Chatbot", **kwargs):
        super().__init__(
            name=name,
            description="A conversational agent that can engage in natural dialogue",
            **kwargs
        )
        self.conversation_history: List[Dict[str, str]] = []
        self.message_bus = MessageBus()
    
    async def initialize(self) -> None:
        """Initialize the chatbot"""
        await super().initialize()
        await self.message_bus.start()
        
        # Subscribe to user messages
        self.message_bus.subscribe_to_commands(
            self.id,
            "chat.*",
            self._handle_message
        )
    
    @cache_response(ttl=3600)
    @with_retry(max_attempts=3)
    @with_telemetry("chat_response")
    async def execute(self, input_data: Any) -> Any:
        """Process user input and generate response"""
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": input_data
        })
        
        # Generate response using the model
        response = await self._generate_response(input_data)
        
        # Add response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        return response
    
    async def _generate_response(self, input_text: str) -> str:
        """Generate response using the language model"""
        messages = [
            {"role": "system", "content": self.description}
        ] + self.conversation_history
        
        response = await self.client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        
        return response.choices[0].message.content
    
    async def _handle_message(self, message: Message) -> None:
        """Handle incoming chat messages"""
        if message.type == MessageType.COMMAND:
            response = await self.execute(message.content)
            
            # Send response back
            await self.message_bus.send_command(
                sender=self.id,
                recipients=[message.sender],
                command="chat.response",
                payload=response
            )
    
    async def cleanup(self) -> None:
        """Cleanup resources"""
        await self.message_bus.stop()
        await super().cleanup()

# Example usage
async def main():
    # Create and initialize chatbot
    chatbot = ChatbotAgent()
    await chatbot.initialize()
    
    try:
        # Example conversation
        responses = []
        for message in [
            "Hello! How are you?",
            "What can you help me with?",
            "Tell me a joke!"
        ]:
            response = await chatbot.execute(message)
            responses.append(response)
            print(f"User: {message}")
            print(f"Chatbot: {response}\n")
    
    finally:
        await chatbot.cleanup()

if __name__ == "__main__":
    asyncio.run(main())