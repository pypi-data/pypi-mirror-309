# AgentSys API Documentation

## Core Components

### BaseAgent

The foundation class for all agents in the framework.

```python
class BaseAgent(BaseModel):
    """Base agent class that defines core functionality"""
    id: str                     # Unique identifier
    name: str                   # Agent name
    description: str            # Agent description
    state: AgentState          # Current execution state
    config: AgentConfig        # Agent configuration
    context: AgentContext      # Execution context
    created_at: datetime       # Creation timestamp
    updated_at: datetime       # Last update timestamp
    tools: List[Callable]      # Available tools/functions
    memory: MemoryManager      # Memory management
```

#### Methods

- `async initialize() -> None`: Initialize agent resources
- `async execute(input_data: Any) -> AgentResponse`: Execute agent's main task with multi-turn support
- `async _run_turn(input_data: Any, messages: List[Dict[str, str]]) -> AgentResponse`: Run a single conversation turn
- `async process_response(response: Any) -> Any`: Process and validate response
- `async handle_error(error: Exception) -> None`: Handle execution errors
- `async cleanup() -> None`: Clean up resources
- `update_context(**kwargs) -> None`: Update agent's context
- `get_context_value(key: str, default: Any = None) -> Any`: Get context value

### AgentConfig

Configuration for agent behavior.

```python
class AgentConfig(BaseModel):
    """Configuration for an agent"""
    model: str = "gpt-4"              # Model identifier
    temperature: float = 0.7          # Response temperature
    max_tokens: Optional[int] = None  # Max response tokens
    stream: bool = False              # Enable streaming
    timeout: float = 60.0            # Operation timeout
    memory_size: int = 1000          # Working memory size
    storage_path: Optional[str] = None # Long-term memory path
    max_turns: int = 10              # Maximum conversation turns
    execute_tools: bool = True       # Whether to execute tool calls
```

### AgentContext

Context information for agent execution.

```python
class AgentContext(BaseModel):
    """Context information for agent execution"""
    variables: Dict[str, Any] = Field(default_factory=dict)
    memory: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
```

### ToolCall

Represents a tool/function call made by an agent.

```python
class ToolCall(BaseModel):
    """Represents a tool/function call"""
    name: str                   # Tool name
    arguments: Dict[str, Any]   # Tool arguments
    result: Optional[Any] = None # Tool execution result
```

### AgentResponse

Response from an agent execution.

```python
class AgentResponse(BaseModel):
    """Response from an agent execution"""
    messages: List[Dict[str, str]]   # Conversation messages
    agent: BaseAgent                 # Responding agent
    context: AgentContext           # Updated context
    tool_calls: List[ToolCall]      # Tool calls made
    next_agent: Optional[BaseAgent] = None  # Next agent to handle task
```

### TaskAgent

Base class for implementing task-specific agents.

```python
class TaskAgent(BaseAgent):
    """Agent specialized for specific tasks"""
    task_description: str       # Description of the task
```

#### Methods

- `async _run_turn(input_data: Any, messages: List[Dict[str, str]]) -> AgentResponse`: Handle a single conversation turn
- `async _run_task(input_data: Any) -> Any`: Internal task implementation

### Memory Management

The framework includes built-in memory management:

```python
class MemoryManager:
    """Manages agent memory"""
    def __init__(self, working_memory: WorkingMemory, 
                 long_term_memory: Optional[LongTermMemory] = None):
        self.working_memory = working_memory
        self.long_term_memory = long_term_memory

class WorkingMemory:
    """Short-term working memory"""
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        
class LongTermMemory:
    """Persistent long-term memory"""
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
```

## Usage Examples

### Creating a Custom Agent

```python
from agentsys import BaseAgent, AgentConfig, AgentContext

class CustomAgent(BaseAgent):
    async def _run_turn(self, input_data: Any, 
                       messages: List[Dict[str, str]]) -> AgentResponse:
        # Process input data
        result = await self._process(input_data)
        
        # Update messages
        messages.append({
            "role": "assistant",
            "content": str(result)
        })
        
        # Return response
        return AgentResponse(
            messages=messages,
            agent=self,
            context=self.context,
            tool_calls=[]
        )
        
    async def _process(self, data: Any) -> Any:
        # Implement processing logic
        return processed_data
```

### Using Tools

```python
from agentsys import TaskAgent, ToolCall

class ToolAgent(TaskAgent):
    async def _run_task(self, input_data: Any) -> Any:
        # Create tool call
        tool_call = ToolCall(
            name="process_data",
            arguments={"data": input_data}
        )
        
        # Execute tool if enabled
        if self.config.execute_tools:
            tool = next(t for t in self.tools 
                       if t.__name__ == tool_call.name)
            tool_call.result = await tool(**tool_call.arguments)
        
        return tool_call.result
```

### Memory Usage

```python
from agentsys import TaskAgent, WorkingMemory, LongTermMemory

class MemoryAgent(TaskAgent):
    async def initialize(self) -> None:
        # Initialize with both working and long-term memory
        self.memory = MemoryManager(
            working_memory=WorkingMemory(max_size=1000),
            long_term_memory=LongTermMemory(
                storage_path="./agent_memory"
            )
        )
    
    async def _run_task(self, input_data: Any) -> Any:
        # Use working memory
        self.memory.working_memory.add(input_data)
        
        # Use long-term memory if available
        if self.memory.long_term_memory:
            await self.memory.long_term_memory.store(input_data)
        
        return processed_result
```

## Best Practices

### Memory Usage

1. Use working memory for temporary data:
```python
await self.memory.working_memory.store(
    "temp_key",
    temporary_data,
    source="calculation"
)
```

2. Use long-term memory for persistence:
```python
if self.memory.long_term_memory:
    await self.memory.long_term_memory.store(
        "permanent_key",
        important_data,
        category="results"
    )
```

### Error Handling

1. Use the built-in error handling:
```python
try:
    result = await self._run_task(input_data)
    return result
except Exception as e:
    await self.handle_error(e)
```

2. Custom error handling:
```python
async def handle_error(self, error: Exception) -> None:
    self.state = AgentState.ERROR
    # Custom error handling
    await self.cleanup()
    raise error
```

### State Management

1. Update state appropriately:
```python
async def custom_operation(self):
    self.state = AgentState.RUNNING
    try:
        result = await self._process()
        self.state = AgentState.COMPLETED
        return result
    except Exception as e:
        self.state = AgentState.ERROR
        raise e
```

### Context Management

1. Use context for shared data:
```python
def setup_context(self):
    self.update_context(
        session_id=str(uuid.uuid4()),
        start_time=datetime.utcnow()
    )
```

2. Access context values:
```python
session_id = self.get_context_value("session_id")
if session_id:
    # Use session_id
    pass
```

## Configuration

### AgentConfig

Configuration options for agents.

```python
class AgentConfig(BaseModel):
    """Agent configuration"""
    model: str = "gpt-4"              # Model identifier
    temperature: float = 0.7          # Response temperature
    max_tokens: Optional[int] = None  # Max response tokens
    stream: bool = False              # Stream responses
    timeout: float = 60.0            # Operation timeout
    memory_size: int = 1000          # Working memory size
    storage_path: Optional[str] = None # Long-term storage path
    max_turns: int = 10              # Maximum conversation turns
    execute_tools: bool = True       # Whether to execute tool calls
```

### AgentContext

Execution context for agents.

```python
class AgentContext(BaseModel):
    """Context information for agent execution"""
    variables: Dict[str, Any] = Field(default_factory=dict)
    memory: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
```

## States

### AgentState

Possible agent execution states.

```python
class AgentState(str, Enum):
    """Agent states"""
    IDLE = "idle"           # Not processing
    RUNNING = "running"     # Currently processing
    PAUSED = "paused"      # Temporarily paused
    ERROR = "error"        # Error occurred
    COMPLETED = "completed" # Task completed
