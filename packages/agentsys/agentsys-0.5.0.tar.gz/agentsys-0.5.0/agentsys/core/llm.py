"""LLM integration module for AgentSys"""

from typing import Dict, List, Optional, Any, AsyncGenerator
from pydantic import BaseModel, Field
import aiohttp
import json
import os
import logging
from ..config.settings import config

logger = logging.getLogger(__name__)

class LLMConfig(BaseModel):
    """Configuration for LLM integration"""
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    stream: bool = False
    timeout: float = 60.0
    api_key: Optional[str] = None
    api_base: str = "https://api.openai.com/v1"

class LLMResponse(BaseModel):
    """Response from LLM"""
    content: str
    role: str = "assistant"
    tool_calls: List[Dict[str, Any]] = Field(default_factory=list)
    finish_reason: Optional[str] = None
    usage: Optional[Dict[str, int]] = None

class LLMClient:
    """Client for interacting with LLMs"""
    
    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or LLMConfig()
        self.api_key = (
            self.config.api_key or 
            os.environ.get("OPENAI_API_KEY") or 
            config.agent.get("api_key")
        )
        if not self.api_key:
            raise ValueError("OpenAI API key not found")
        
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def initialize(self) -> None:
        """Initialize the client"""
        if self._session is None:
            self._session = aiohttp.ClientSession(
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
    
    async def cleanup(self) -> None:
        """Cleanup resources"""
        if self._session:
            await self._session.close()
            self._session = None
    
    async def __aenter__(self) -> "LLMClient":
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.cleanup()
    
    async def complete(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> LLMResponse:
        """Complete a conversation"""
        if self._session is None:
            await self.initialize()
        
        # Prepare request
        url = f"{self.config.api_base}/chat/completions"
        data = {
            "model": self.config.model,
            "messages": messages,
            "temperature": self.config.temperature,
            "stream": self.config.stream
        }
        
        # Add optional parameters
        if self.config.max_tokens:
            data["max_tokens"] = self.config.max_tokens
        if tools:
            data["tools"] = tools
            data["tool_choice"] = "auto"
        
        # Override with kwargs
        data.update(kwargs)
        
        try:
            async with self._session.post(url, json=data) as response:
                if response.status != 200:
                    error_data = await response.text()
                    raise ValueError(f"OpenAI API error: {error_data}")
                
                result = await response.json()
                
                # Extract response
                choice = result["choices"][0]
                message = choice["message"]
                
                return LLMResponse(
                    content=message.get("content", ""),
                    role=message.get("role", "assistant"),
                    tool_calls=message.get("tool_calls", []),
                    finish_reason=choice.get("finish_reason"),
                    usage=result.get("usage")
                )
        
        except aiohttp.ClientError as e:
            logger.error(f"OpenAI API request failed: {str(e)}")
            raise
    
    async def stream_complete(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> AsyncGenerator[LLMResponse, None]:
        """Stream completions from the model"""
        if self._session is None:
            await self.initialize()
        
        # Prepare request
        url = f"{self.config.api_base}/chat/completions"
        data = {
            "model": self.config.model,
            "messages": messages,
            "temperature": self.config.temperature,
            "stream": True  # Force streaming
        }
        
        # Add optional parameters
        if self.config.max_tokens:
            data["max_tokens"] = self.config.max_tokens
        if tools:
            data["tools"] = tools
            data["tool_choice"] = "auto"
        
        # Override with kwargs
        data.update(kwargs)
        
        try:
            async with self._session.post(url, json=data) as response:
                if response.status != 200:
                    error_data = await response.text()
                    raise ValueError(f"OpenAI API error: {error_data}")
                
                # Process streaming response
                current_content = ""
                current_tool_calls = []
                
                async for line in response.content:
                    line = line.strip()
                    if not line or line == b"data: [DONE]":
                        continue
                    
                    # Parse SSE data
                    try:
                        line = line.decode("utf-8")
                        if not line.startswith("data: "):
                            continue
                        
                        data = json.loads(line[6:])
                        delta = data["choices"][0]["delta"]
                        
                        # Update content
                        if "content" in delta:
                            current_content += delta["content"]
                        
                        # Update tool calls
                        if "tool_calls" in delta:
                            current_tool_calls.extend(delta["tool_calls"])
                        
                        # Yield response
                        yield LLMResponse(
                            content=current_content,
                            role="assistant",
                            tool_calls=current_tool_calls,
                            finish_reason=data["choices"][0].get("finish_reason")
                        )
                    
                    except json.JSONDecodeError:
                        continue
        
        except aiohttp.ClientError as e:
            logger.error(f"OpenAI API streaming request failed: {str(e)}")
            raise
