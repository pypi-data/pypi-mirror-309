"""Agent client module for AgentSys"""

from typing import Dict, List, Optional, Any, AsyncGenerator
from pydantic import BaseModel, Field
from openai import AsyncOpenAI
import json
import logging
from ..config.settings import config
from locksys import Locksys

logger = logging.getLogger(__name__)

class AgentConfig(BaseModel):
    """Configuration for agent client"""
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    stream: bool = False
    timeout: float = 60.0
    vault: str = "API"
    item: str
    key: str
    url: Optional[str] = None
    api_base: str = "https://api.openai.com/v1"

class TokenUsage(BaseModel):
    """Token usage information"""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

class AgentResponse(BaseModel):
    """Response from agent"""
    content: str
    role: str = "assistant"
    tool_calls: List[Dict[str, Any]] = Field(default_factory=list)
    finish_reason: Optional[str] = None
    usage: Optional[TokenUsage] = None

class AgentClient:
    """Client for interacting with LLM APIs"""
    
    def __init__(self, config: Optional[AgentConfig] = None):
        self.config = config or AgentConfig()
        self.api_key = Locksys(self.config.vault).item(self.config.item).key(self.config.key).results()
        if not self.api_key:
            raise ValueError("API key not found in Locksys")
        
        self._client: Optional[AsyncOpenAI] = None
    
    async def initialize(self) -> None:
        """Initialize the client"""
        if self._client is None:
            self._client = AsyncOpenAI(
                api_key=self.api_key,
                base_url=self.config.url if self.config.url else self.config.api_base
            )
    
    async def cleanup(self) -> None:
        """Cleanup resources"""
        if self._client:
            await self._client.close()
            self._client = None
    
    async def __aenter__(self) -> "AgentClient":
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.cleanup()
    
    async def complete(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> AgentResponse:
        """Complete a conversation"""
        if self._client is None:
            await self.initialize()
        
        try:
            completion = await self._client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                stream=self.config.stream,
                tools=tools,
                tool_choice="auto" if tools else None,
                **kwargs
            )
            
            # Extract response
            choice = completion.choices[0]
            message = choice.message
            
            # Create token usage
            usage = None
            if completion.usage:
                usage = TokenUsage(
                    prompt_tokens=completion.usage.prompt_tokens,
                    completion_tokens=completion.usage.completion_tokens,
                    total_tokens=completion.usage.total_tokens
                )
            
            return AgentResponse(
                content=message.content or "",
                role=message.role,
                tool_calls=[
                    tool_call.model_dump() 
                    for tool_call in (message.tool_calls or [])
                ],
                finish_reason=choice.finish_reason,
                usage=usage
            )
        
        except Exception as e:
            logger.error(f"API request failed: {str(e)}")
            raise
    
    async def stream_complete(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> AsyncGenerator[AgentResponse, None]:
        """Stream completions from the model"""
        if self._client is None:
            await self.initialize()
        
        try:
            stream = await self._client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                stream=True,
                tools=tools,
                tool_choice="auto" if tools else None,
                **kwargs
            )
            
            current_content = ""
            current_tool_calls = []
            
            async for chunk in stream:
                delta = chunk.choices[0].delta
                
                # Update content
                if delta.content:
                    current_content += delta.content
                
                # Update tool calls
                if delta.tool_calls:
                    for tool_call in delta.tool_calls:
                        current_tool_calls.append(tool_call.model_dump())
                
                # Yield response
                yield AgentResponse(
                    content=current_content,
                    role="assistant",
                    tool_calls=current_tool_calls,
                    finish_reason=chunk.choices[0].finish_reason
                )
        
        except Exception as e:
            logger.error(f"API streaming request failed: {str(e)}")
            raise
