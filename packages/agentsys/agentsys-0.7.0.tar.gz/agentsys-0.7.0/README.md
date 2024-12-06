![AgentSys Logo](assets/logo.png)

# AgentSys (experimental, educational)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> AgentSys is currently an experimental sample framework intended to explore ergonomic interfaces for multi-agent systems. It is not intended to be used in production, and therefore has no official support. (This also means we will not be reviewing PRs or issues!)

> The primary goal of AgentSys is to showcase the handoff & routines patterns explored in the [Orchestrating Agents: Handoffs & Routines](https://cookbook.openai.com/examples/orchestrating_agents) cookbook. It is not meant as a standalone library, and is primarily for educational purposes.

## Installation

### SSH

```bash
pip install git+ssh://git@github.com/lifsys/agentsys.git
```

### HTTPS

```bash
pip install git+https://github.com/lifsys/agentsys.git
```

## Project Structure

The project is organized into several key modules:

- `agentsys.orchestration`: Core orchestration functionality
  - `Swarm`: Main orchestration class for managing agent interactions
  - `Agent`: Base class for defining agents
- `agentsys.models`: Model interfaces and implementations
  - `BaseModel`: Abstract base class for model implementations
  - `OpenAIModel`: OpenAI model implementation
- `agentsys.config`: Configuration management
  - `Settings`: Configuration settings and utilities
- `agentsys.types`: Type definitions and data structures
- `agentsys.util`: Utility functions and helpers

## Basic Usage

```python
from agentsys import Swarm, Agent

client = Swarm()
agent = Agent(
    name="test",
    instructions="You are a helpful assistant.",
    model="gpt-4",
)

messages = [{"role": "user", "content": "Hello!"}]
response = client.run(agent, messages)
print(response.messages[-1]["content"])
```

## Function Calling

AgentSys supports function calling with both OpenAI's function calling and tool calling APIs:

```python
def get_weather(location: str) -> str:
    """Get the weather for a location."""
    return f"The weather in {location} is sunny!"

agent = Agent(
    name="weather",
    instructions="You can help users check the weather.",
    model="gpt-4",
    functions=[get_weather],
)

messages = [{"role": "user", "content": "What's the weather in San Francisco?"}]
response = client.run(agent, messages)
print(response.messages[-1]["content"])
```

## Configuration

You can configure AgentSys using environment variables or by passing a config object:

```python
from agentsys import Settings

settings = Settings(
    openai_api_key="your-api-key",
    temperature=0.7,
)
```

### Swarm Client

The `Swarm` class is the main entry point for interacting with agents. It handles:

- Message routing
- Function calling
- Response streaming
- Error handling

## Contributing

This is an experimental project and we are not accepting contributions at this time.

## License

MIT
