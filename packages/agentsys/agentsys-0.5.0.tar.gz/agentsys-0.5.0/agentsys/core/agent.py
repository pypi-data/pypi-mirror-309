"""Core agent framework implementation"""

from typing import Dict, List, Optional, Any, Callable, Union
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
import uuid
import asyncio
from datetime import datetime
from .memory import WorkingMemory, LongTermMemory, MemoryManager
from .agentClient import AgentClient, AgentConfig as ClientConfig, AgentResponse as ClientResponse

class AgentState(str, Enum):
    """Agent execution states"""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    ERROR = "error"
    COMPLETED = "completed"

class AgentContext(BaseModel):
    """Context information for agent execution"""
    variables: Dict[str, Any] = Field(default_factory=dict)
    memory: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

class AgentConfig(BaseModel):
    """Configuration for an agent"""
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    stream: bool = False
    timeout: float = 60.0
    memory_size: int = 1000
    storage_path: Optional[str] = None
    max_turns: int = 10  # Maximum conversation turns
    execute_tools: bool = True  # Whether to execute tool calls
    vault: str = "API"  # Locksys vault
    item: str = "openai"  # Locksys item
    key: str = "api_key"  # Locksys key
    url: Optional[str] = None  # Optional API URL
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

class ToolCall(BaseModel):
    """Represents a tool/function call"""
    name: str
    arguments: Dict[str, Any]
    result: Optional[Any] = None

class AgentResponse(BaseModel):
    """Response from an agent execution"""
    messages: List[Dict[str, str]]
    agent: 'BaseAgent'
    context: AgentContext
    tool_calls: List[ToolCall] = Field(default_factory=list)
    next_agent: Optional['BaseAgent'] = None

class BaseAgent(BaseModel):
    """Base agent class that defines core functionality"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    state: AgentState = AgentState.IDLE
    config: AgentConfig = Field(default_factory=AgentConfig)
    context: AgentContext = Field(default_factory=AgentContext)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    tools: List[Callable] = Field(default_factory=list)
    memory: Optional[MemoryManager] = None
    client: Optional[AgentClient] = None
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, **data):
        super().__init__(**data)
        self.memory = MemoryManager(
            working_memory=WorkingMemory(max_size=self.config.memory_size),
            long_term_memory=LongTermMemory(storage_path=self.config.storage_path) if self.config.storage_path else None
        )
        self.client = AgentClient(ClientConfig(
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            stream=self.config.stream,
            timeout=self.config.timeout,
            vault=self.config.vault,
            item=self.config.item,
            key=self.config.key,
            url=self.config.url
        ))

    async def initialize(self) -> None:
        """Initialize agent resources"""
        await self.client.initialize()

    async def execute(self, input_data: Any) -> AgentResponse:
        """Execute agent's main task with multi-turn support"""
        try:
            self.state = AgentState.RUNNING
            turn_count = 0
            current_agent = self
            current_messages = []
            
            while turn_count < self.config.max_turns:
                # Run one turn
                response = await current_agent._run_turn(
                    input_data, 
                    current_messages
                )
                
                # Update messages
                current_messages = response.messages
                
                # Execute tools if enabled
                if self.config.execute_tools and response.tool_calls:
                    for tool_call in response.tool_calls:
                        if tool_call.name in [t.__name__ for t in self.tools]:
                            tool = next(t for t in self.tools if t.__name__ == tool_call.name)
                            tool_call.result = await tool(**tool_call.arguments)
                            
                            # Check if tool returned a new agent
                            if isinstance(tool_call.result, BaseAgent):
                                response.next_agent = tool_call.result
                
                # Handle agent handoff
                if response.next_agent:
                    current_agent = response.next_agent
                    await current_agent.initialize()
                    
                    # Update context
                    current_agent.context = response.context
                    
                    # Continue with new agent
                    continue
                
                # No more tools or handoffs, we're done
                if not response.tool_calls:
                    break
                
                turn_count += 1
            
            self.state = AgentState.COMPLETED
            return response
            
        except Exception as e:
            await self.handle_error(e)
        finally:
            await self.cleanup()

    async def _run_turn(self, input_data: Any, 
                       messages: List[Dict[str, str]]) -> AgentResponse:
        """Run a single conversation turn"""
        # Add user input to messages
        messages.append({
            "role": "user",
            "content": str(input_data)
        })
        
        # Prepare tools format for OpenAI
        tools_format = []
        for tool in self.tools:
            tools_format.append({
                "type": "function",
                "function": {
                    "name": tool.__name__,
                    "description": tool.__doc__ or "",
                    "parameters": {
                        "type": "object",
                        "properties": {},  # TODO: Extract from type hints
                        "required": []
                    }
                }
            })
        
        # Get completion from client
        client_response = await self.client.complete(
            messages=messages,
            tools=tools_format if self.tools else None
        )
        
        # Add assistant response to messages
        messages.append({
            "role": client_response.role,
            "content": client_response.content
        })
        
        # Convert tool calls
        tool_calls = []
        for tool_call in client_response.tool_calls:
            tool_calls.append(ToolCall(
                name=tool_call["function"]["name"],
                arguments=tool_call["function"]["arguments"]
            ))
        
        return AgentResponse(
            messages=messages,
            agent=self,
            context=self.context,
            tool_calls=tool_calls
        )

    async def process_response(self, response: Any) -> Any:
        """Process and validate agent's response"""
        return response

    async def handle_error(self, error: Exception) -> None:
        """Handle errors during execution"""
        self.state = AgentState.ERROR
        raise error

    async def cleanup(self) -> None:
        """Cleanup resources"""
        if self.client:
            await self.client.cleanup()

    def update_context(self, **kwargs) -> None:
        """Update agent's context"""
        self.context.variables.update(kwargs)
        self.updated_at = datetime.utcnow()

    def get_context_value(self, key: str, default: Any = None) -> Any:
        """Get value from agent's context"""
        return self.context.variables.get(key, default)

class TaskAgent(BaseAgent):
    """Agent specialized for specific tasks"""
    task_description: str
    
    async def _run_turn(self, input_data: Any, 
                       messages: List[Dict[str, str]]) -> AgentResponse:
        """Run a single conversation turn"""
        try:
            # Process the task
            result = await self._run_task(input_data)
            
            # Create response
            messages.append({
                "role": "assistant",
                "content": str(result)
            })
            
            return AgentResponse(
                messages=messages,
                agent=self,
                context=self.context
            )
            
        except Exception as e:
            await self.handle_error(e)

    async def _run_task(self, input_data: Any) -> Any:
        """Internal method to run the task"""
        raise NotImplementedError("Subclasses must implement _run_task method")