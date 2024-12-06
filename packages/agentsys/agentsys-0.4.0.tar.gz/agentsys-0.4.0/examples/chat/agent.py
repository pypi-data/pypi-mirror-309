"""
Example implementation of a ChatAgent using the AgentSys framework.
"""

from typing import List, Dict, Any
import asyncio
import aiohttp
from datetime import datetime
from locksys import Locksys
from agentsys.core.agent import TaskAgent
from agentsys.core.memory import MemoryManager, WorkingMemory, LongTermMemory
from pydantic import Field

class ChatAgent(TaskAgent):
    """Agent specialized for chat interactions using OpenAI API"""
    instructions: str = "You are a helpful agent."
    messages: List[Dict[str, str]] = Field(default_factory=list)
    api_key: str = Field(default_factory=lambda: Locksys().item("OPEN-AI").key("Mamba").results())
    memory: MemoryManager = None  # Will be initialized in __init__
    
    def __init__(self, **data):
        super().__init__(**data)
        self.memory = MemoryManager(
            working_memory=WorkingMemory(max_size=self.config.memory_size),
            long_term_memory=LongTermMemory(storage_path=self.config.storage_path) if self.config.storage_path else None
        )
    
    async def _run_task(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Run a chat completion task"""
        # Store the conversation in memory
        memory_key = f"conversation_{datetime.utcnow().isoformat()}"
        await self.memory.working_memory.store(memory_key, messages)
        
        full_messages = [{"role": "system", "content": self.instructions}] + messages
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.config.model,
                    "messages": full_messages,
                    "temperature": self.config.temperature,
                    "max_tokens": self.config.max_tokens
                }
            ) as response:
                result = await response.json()
                response_data = {
                    "messages": messages + [{"role": "assistant", "content": result["choices"][0]["message"]["content"]}]
                }
                
                # Store the response in long-term memory if available
                if self.memory.long_term_memory:
                    await self.memory.long_term_memory.store(
                        memory_key,
                        response_data,
                        model=self.config.model,
                        temperature=self.config.temperature
                    )
                
                return response_data
    
    def run(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Synchronous wrapper for chat completion"""
        return asyncio.run(self.execute(messages))
