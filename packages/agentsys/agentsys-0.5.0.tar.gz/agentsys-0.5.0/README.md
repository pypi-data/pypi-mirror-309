# AgentSys Framework

A robust, extensible framework for building AI agents with memory, state management, and middleware capabilities.

## Features

- **Flexible Agent Architecture**
  - BaseAgent: Core functionality and lifecycle management
  - TaskAgent: Task-specific agent implementation base
  - Memory System: Both working and long-term storage
  - State Management: Full agent lifecycle control

- **Extensible Components**
  - Middleware: Caching, retries, and telemetry
  - Plugins: Routing and storage backends
  - Protocols: Messaging and streaming support
  - Configuration: Flexible settings management

- **Built-in Memory Management**
  - Working Memory: Fast, in-memory storage
  - Long-term Memory: Persistent storage with JSON serialization
  - Memory Manager: Unified memory interface

## Documentation

- [**Core API**](docs/api.md): Comprehensive guide to BaseAgent, TaskAgent, and the memory system. Learn how to create custom agents and manage state.
- [**Middleware**](docs/middleware.md): Cache responses, implement retries, and monitor performance with the middleware system.
- [**Plugins**](docs/plugins.md): Extend functionality with routing and storage plugins. Build custom plugins for your specific needs.
- [**Protocols**](docs/protocols.md): Implement inter-agent communication and real-time data streaming with the protocol system.

## Installation

```bash
pip install agentsys
```

## Quick Start

```python
from agentsys.core import TaskAgent
from typing import Any

class MyAgent(TaskAgent):
    async def _run_task(self, input_data: Any) -> Any:
        # Implement your agent's logic here
        return processed_result

# Create and use your agent
agent = MyAgent(
    name="MyAgent",
    description="A custom agent",
    task_description="Process specific tasks"
)

result = await agent.execute(input_data)
```

## Framework Components

### Core (agentsys.core)

- **BaseAgent**: Foundation class with lifecycle management
- **TaskAgent**: Base class for task-specific agents
- **Memory System**: Working and long-term memory management

### Middleware (agentsys.middleware)

- **Cache**: Response caching for performance
- **Retry**: Automatic retry logic
- **Telemetry**: Performance monitoring

### Plugins (agentsys.plugins)

- **Router**: Agent communication and task routing
- **Storage**: Custom storage backends

### Protocols (agentsys.protocols)

- **Messaging**: Inter-agent communication
- **Streaming**: Real-time data handling

## Example Implementations

Check the `examples/` directory for various agent implementations:

- **ChatAgent**: OpenAI-powered chat agent
- **More examples coming soon**

## Building Custom Agents

1. **Inherit from TaskAgent**:
```python
class CustomAgent(TaskAgent):
    async def _run_task(self, input_data: Any) -> Any:
        # Your implementation here
        pass
```

2. **Use Memory**:
```python
# Store in working memory
await self.memory.working_memory.store("key", value)

# Store in long-term memory
if self.memory.long_term_memory:
    await self.memory.long_term_memory.store("key", value)
```

3. **Handle State**:
```python
# State is automatically managed in execute()
try:
    self.state = AgentState.RUNNING
    result = await self._run_task(input_data)
    self.state = AgentState.COMPLETED
    return result
except Exception as e:
    self.state = AgentState.ERROR
    raise e
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details
