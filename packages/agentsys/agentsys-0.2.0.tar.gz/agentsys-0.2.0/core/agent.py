from typing import Dict, List, Optional, Any, Callable
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
import uuid
import asyncio
from datetime import datetime

class AgentState(str, Enum):
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
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

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
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

    async def initialize(self) -> None:
        """Initialize agent resources"""
        pass

    async def execute(self, input_data: Any) -> Any:
        """Execute agent's main task"""
        raise NotImplementedError("Subclasses must implement execute method")

    async def process_response(self, response: Any) -> Any:
        """Process and validate agent's response"""
        return response

    async def handle_error(self, error: Exception) -> None:
        """Handle errors during execution"""
        self.state = AgentState.ERROR
        raise error

    async def cleanup(self) -> None:
        """Cleanup resources"""
        pass

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
    tools: List[Callable] = Field(default_factory=list)
    
    async def execute(self, input_data: Any) -> Any:
        try:
            self.state = AgentState.RUNNING
            # Implementation will be added for task execution
            result = await self._run_task(input_data)
            self.state = AgentState.COMPLETED
            return result
        except Exception as e:
            await self.handle_error(e)

    async def _run_task(self, input_data: Any) -> Any:
        """Internal method to run the task"""
        raise NotImplementedError("Subclasses must implement _run_task method")