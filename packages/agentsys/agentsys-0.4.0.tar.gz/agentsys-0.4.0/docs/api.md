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

### AgentResponse

Response from an agent execution.

```python
class AgentResponse(BaseModel):
    """Response from an agent execution"""
    messages: List[Dict[str, str]]  # Conversation messages
    agent: BaseAgent               # Current agent
    context: AgentContext         # Current context
    tool_calls: List[ToolCall]    # Tool calls made
    next_agent: Optional[BaseAgent] # Next agent if handoff
```

### ToolCall

Represents a tool/function call.

```python
class ToolCall(BaseModel):
    """Represents a tool/function call"""
    name: str                    # Tool name
    arguments: Dict[str, Any]    # Tool arguments
    result: Optional[Any]        # Tool result
```

## Examples

### 1. Basic Task Agent

```python
from agentsys.core import TaskAgent, AgentConfig

class DataProcessor(TaskAgent):
    async def _run_task(self, input_data: Any) -> Any:
        # Process the data
        result = f"Processed: {input_data}"
        return result

# Create and use the agent
agent = DataProcessor(
    name="Processor",
    description="Process data",
    task_description="Process input data",
    config=AgentConfig(max_turns=1)
)

response = await agent.execute("test data")
print(response.messages[-1]["content"])  # "Processed: test data"
```

### 2. Multi-turn Agent with Tools

```python
from agentsys.core import TaskAgent, AgentConfig
import aiohttp

class WeatherAgent(TaskAgent):
    async def get_weather(self, city: str) -> str:
        """Get weather for a city"""
        return f"Weather in {city}: Sunny"
    
    async def format_response(self, weather: str) -> str:
        """Format weather response"""
        return f"Here's the forecast: {weather}"
    
    async def _run_task(self, input_data: str) -> Any:
        # Add tools
        self.tools = [self.get_weather, self.format_response]
        
        # Create tool calls
        weather = await self.get_weather("New York")
        response = await self.format_response(weather)
        return response

# Create and use the agent
agent = WeatherAgent(
    name="WeatherBot",
    description="Get weather info",
    task_description="Provide weather forecasts",
    config=AgentConfig(max_turns=2)
)

response = await agent.execute("What's the weather?")
print(response.messages[-1]["content"])
```

### 3. Agent Handoff Example

```python
from agentsys.core import TaskAgent, AgentConfig

class SupportAgent(TaskAgent):
    async def _run_task(self, input_data: str) -> Any:
        return "I'm the support agent, how can I help?"

class SalesAgent(TaskAgent):
    async def transfer_to_support(self) -> SupportAgent:
        """Transfer to support agent"""
        return SupportAgent(
            name="Support",
            description="Help with support",
            task_description="Provide customer support"
        )
    
    async def _run_task(self, input_data: str) -> Any:
        if "help" in input_data.lower():
            # Add transfer tool
            self.tools = [self.transfer_to_support]
            # Call it
            return await self.transfer_to_support()
        return "I'm the sales agent, want to buy something?"

# Create and use the agent
agent = SalesAgent(
    name="Sales",
    description="Handle sales",
    task_description="Process sales inquiries",
    config=AgentConfig(max_turns=3)
)

# This will start with sales and hand off to support
response = await agent.execute("I need help")
print(response.messages[-1]["content"])
```

### 4. Context Management Example

```python
from agentsys.core import TaskAgent, AgentConfig

class ContextAwareAgent(TaskAgent):
    async def _run_task(self, input_data: str) -> Any:
        # Get user info from context
        user_name = self.get_context_value("user_name", "Guest")
        
        # Update context with new data
        self.update_context(
            last_input=input_data,
            interaction_count=self.get_context_value("interaction_count", 0) + 1
        )
        
        return f"Hello {user_name}, this is interaction #{self.context.variables['interaction_count']}"

# Create and use the agent
agent = ContextAwareAgent(
    name="ContextBot",
    description="Context-aware bot",
    task_description="Handle contextual interactions"
)

# First interaction
response = await agent.execute(
    "Hi!",
    context_variables={"user_name": "John"}
)
print(response.messages[-1]["content"])  # "Hello John, this is interaction #1"

# Second interaction (context persists)
response = await agent.execute("Hello again!")
print(response.messages[-1]["content"])  # "Hello John, this is interaction #2"

## Memory System

### MemoryEntry

Represents a single memory entry with metadata.

```python
class MemoryEntry(BaseModel):
    """Single memory entry"""
    key: str                   # Unique key
    value: Any                 # Stored value
    timestamp: datetime        # Storage timestamp
    metadata: Dict[str, Any]   # Additional metadata
```

### WorkingMemory

Short-term, in-memory storage.

```python
class WorkingMemory(BaseMemory):
    """Short-term memory implementation"""
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
```

#### Methods

- `async store(key: str, value: Any, **metadata) -> None`: Store value
- `async retrieve(key: str) -> Optional[Any]`: Retrieve value
- `async clear() -> None`: Clear all entries

### LongTermMemory

Persistent storage with JSON serialization.

```python
class LongTermMemory(BaseMemory):
    """Persistent memory implementation"""
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
```

#### Methods

- `async store(key: str, value: Any, **metadata) -> None`: Store value
- `async retrieve(key: str) -> Optional[Any]`: Retrieve value
- `async clear() -> None`: Clear all entries

### MemoryManager

Unified interface for memory management.

```python
class MemoryManager:
    """Memory management interface"""
    def __init__(self, working_memory: WorkingMemory, 
                 long_term_memory: Optional[LongTermMemory] = None):
        self.working_memory = working_memory
        self.long_term_memory = long_term_memory
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
    max_turns: int = 1               # Maximum conversation turns
```

### AgentContext

Execution context for agents.

```python
class AgentContext(BaseModel):
    """Context information"""
    variables: Dict[str, Any]         # Context variables
    memory: Dict[str, Any]           # Memory storage
    metadata: Dict[str, Any]         # Additional metadata
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
