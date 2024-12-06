# Plugins Documentation

## Overview

AgentSys plugins extend the framework's functionality:
- Router: Agent communication and task routing
- Storage: Custom storage backends
- Custom plugins: Extend functionality

## Step-by-Step: Building Your First Plugin

Let's build a simple logging plugin that tracks agent activities. We'll create a new plugin package in the framework.

### Step 1: Create Plugin Directory Structure

Create the following directory structure:
```
agentsys/
├── plugins/
│   ├── __init__.py
│   ├── base.py          # Base plugin classes
│   ├── logger/          # Our new logging plugin
│   │   ├── __init__.py
│   │   ├── config.py    # Plugin configuration
│   │   ├── plugin.py    # Plugin implementation
│   │   └── agent.py     # Agent integration
│   └── tests/
│       └── test_logger_plugin.py
```

### Step 2: Define Base Plugin Interface

File: `/Users/lifsys/devhub/agentsys/agentsys/plugins/base.py`
```python
from abc import ABC, abstractmethod
from typing import Any
from pydantic import BaseModel

class PluginConfig(BaseModel):
    """Base configuration for plugins"""
    enabled: bool = True
    name: str = "base_plugin"

class BasePlugin(ABC):
    """Base class for all plugins"""
    
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize plugin resources"""
        pass
    
    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup plugin resources"""
        pass
```

### Step 3: Define Plugin Configuration

File: `/Users/lifsys/devhub/agentsys/agentsys/plugins/logger/config.py`
```python
from ..base import PluginConfig
from pydantic import Field
from typing import Optional

class LoggerConfig(PluginConfig):
    """Configuration for the logging plugin"""
    name: str = "logger_plugin"
    log_file: str = "agent_activities.log"  # Default log file
    log_level: str = "INFO"                 # Logging level
    max_file_size: int = 1024 * 1024       # 1MB default
    backup_count: int = 3                   # Keep 3 backup files
    log_format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
```

### Step 4: Implement Plugin

File: `/Users/lifsys/devhub/agentsys/agentsys/plugins/logger/plugin.py`
```python
from ..base import BasePlugin
from .config import LoggerConfig
from typing import Any
import logging
import os

class LoggerPlugin(BasePlugin):
    """Simple logging plugin for agent activities"""
    
    def __init__(self, config: LoggerConfig):
        self.config = config
        self.logger = None
    
    async def initialize(self) -> None:
        """Setup the logger"""
        # Create logger
        self.logger = logging.getLogger(self.config.name)
        self.logger.setLevel(self.config.log_level)
        
        # Create formatter
        formatter = logging.Formatter(self.config.log_format)
        
        # Create file handler
        handler = logging.FileHandler(self.config.log_file)
        handler.setFormatter(formatter)
        
        # Add handler to logger
        self.logger.addHandler(handler)
    
    async def cleanup(self) -> None:
        """Cleanup resources"""
        if self.logger:
            for handler in self.logger.handlers:
                handler.close()
                self.logger.removeHandler(handler)
    
    async def log_activity(self, agent_name: str, 
                          activity: str, details: Any) -> None:
        """Log an agent activity"""
        if not self.logger:
            await self.initialize()
        
        message = f"Agent '{agent_name}' - {activity}: {details}"
        self.logger.info(message)
    
    async def log_error(self, agent_name: str, 
                       error: Exception) -> None:
        """Log an error"""
        if not self.logger:
            await self.initialize()
        
        message = f"Agent '{agent_name}' encountered error: {str(error)}"
        self.logger.error(message)
```

### Step 5: Create Agent Integration

File: `/Users/lifsys/devhub/agentsys/agentsys/plugins/logger/agent.py`
```python
from agentsys.core import TaskAgent
from .plugin import LoggerPlugin
from .config import LoggerConfig
from typing import Any

class LoggingAgent(TaskAgent):
    """Agent with logging capabilities"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize logger with custom config
        self.logger = LoggerPlugin(
            LoggerConfig(
                name=f"{self.name}_logger",
                log_file=f"{self.name}_activities.log",
                log_level="INFO"
            )
        )
    
    async def initialize(self) -> None:
        """Initialize agent and logger"""
        await super().initialize()
        await self.logger.initialize()
    
    async def _run_task(self, input_data: Any) -> Any:
        """Run task with logging"""
        try:
            # Log task start
            await self.logger.log_activity(
                self.name,
                "task_start",
                f"Input: {input_data}"
            )
            
            # Run the task
            result = await self._process(input_data)
            
            # Log task completion
            await self.logger.log_activity(
                self.name,
                "task_complete",
                f"Result: {result}"
            )
            
            return result
            
        except Exception as e:
            # Log any errors
            await self.logger.log_error(self.name, e)
            raise
```

### Step 6: Add Plugin Tests

File: `/Users/lifsys/devhub/agentsys/agentsys/plugins/tests/test_logger_plugin.py`
```python
import pytest
import os
from ..logger.plugin import LoggerPlugin
from ..logger.config import LoggerConfig

@pytest.fixture
async def logger():
    """Setup and cleanup logger for tests"""
    config = LoggerConfig(
        name="test_logger",
        log_file="test.log"
    )
    plugin = LoggerPlugin(config)
    await plugin.initialize()
    yield plugin
    await plugin.cleanup()
    if os.path.exists("test.log"):
        os.remove("test.log")

@pytest.mark.asyncio
async def test_log_activity(logger):
    """Test basic logging functionality"""
    await logger.log_activity(
        "TestAgent",
        "test_action",
        "test details"
    )
    
    with open("test.log", "r") as f:
        log_content = f.read()
        assert "TestAgent" in log_content
        assert "test_action" in log_content

@pytest.mark.asyncio
async def test_log_error(logger):
    """Test error logging"""
    test_error = ValueError("Test error")
    await logger.log_error("TestAgent", test_error)
    
    with open("test.log", "r") as f:
        log_content = f.read()
        assert "TestAgent" in log_content
        assert "Test error" in log_content
```

### Step 7: Update Plugin Registry

File: `/Users/lifsys/devhub/agentsys/agentsys/plugins/__init__.py`
```python
"""AgentSys plugin system"""

from .base import BasePlugin, PluginConfig
from .logger.plugin import LoggerPlugin
from .logger.config import LoggerConfig
from .logger.agent import LoggingAgent

__all__ = [
    'BasePlugin',
    'PluginConfig',
    'LoggerPlugin',
    'LoggerConfig',
    'LoggingAgent'
]
```

### Step 8: Usage Example

File: `/Users/lifsys/devhub/agentsys/examples/logging_agent.py`
```python
"""Example using the logging plugin"""

import asyncio
from agentsys.plugins import LoggingAgent

async def main():
    # Create logging agent
    agent = LoggingAgent(
        name="DataProcessor",
        description="Process data with logging",
        task_description="Process data and log activities"
    )
    
    # Initialize agent (and plugin)
    await agent.initialize()
    
    try:
        # Run a task
        result = await agent.execute({"data": "test"})
        
        # Check the log file
        with open(f"DataProcessor_activities.log", "r") as f:
            logs = f.read()
            print("Activity Logs:", logs)
            
    finally:
        # Cleanup
        await agent.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
```

### Step 9: Run Tests

```bash
# From the agentsys root directory
pytest agentsys/plugins/tests/test_logger_plugin.py -v
```

## Plugin Development Best Practices

1. **Clear Configuration**
   - Use Pydantic models for configuration
   - Provide sensible defaults
   - Document all configuration options

2. **Proper Resource Management**
   - Initialize resources in `initialize()`
   - Clean up in `cleanup()`
   - Use async context managers when possible

3. **Error Handling**
   - Handle initialization errors gracefully
   - Provide meaningful error messages
   - Log errors appropriately

4. **Testing**
   - Write unit tests for all functionality
   - Use fixtures for setup/cleanup
   - Test error conditions

5. **Documentation**
   - Document configuration options
   - Provide usage examples
   - Include type hints

## Next Steps

After creating your basic plugin:

1. **Add Advanced Features**
   - Add rotation for log files
   - Implement different log formats
   - Add filtering capabilities

2. **Enhance Integration**
   - Create decorators for easy logging
   - Add context managers
   - Implement async streams

3. **Improve Error Handling**
   - Add retry mechanisms
   - Implement fallback options
   - Add error reporting

## Router Plugin

Manages agent communication and task routing.

```python
from agentsys.plugins.router import AgentRouter, RoutingConfig
from typing import Any

# Configure router
router = AgentRouter(
    config=RoutingConfig(
        strategy="round_robin",
        timeout=60
    )
)

# Register agents
await router.register_agent(agent1)
await router.register_agent(agent2)

# Define routes
@router.route("process_data")
async def process_data(input_data: Any) -> Any:
    return await agent1.execute(input_data)

# Route tasks
result = await router.route_task(
    route_key="process_data",
    input_data=data
)
```

### Routing Strategies

1. Round Robin:
```python
router = AgentRouter(
    config=RoutingConfig(strategy="round_robin")
)
```

2. Least Loaded:
```python
router = AgentRouter(
    config=RoutingConfig(strategy="least_loaded")
)
```

3. Custom Strategy:
```python
class CustomStrategy(RoutingStrategy):
    async def select_agent(self, agents: List[Agent],
                          task: Any) -> Agent:
        # Custom selection logic
        return selected_agent

router = AgentRouter(
    config=RoutingConfig(
        strategy=CustomStrategy()
    )
)
```

## Storage Plugin

Custom storage backends for agent data.

```python
from agentsys.plugins.storage import StorageBackend, StorageConfig
from typing import Any, Optional

class CustomStorage(StorageBackend):
    def __init__(self, config: StorageConfig):
        self.config = config
        self.connection = None
    
    async def connect(self) -> None:
        # Initialize connection
        pass
    
    async def disconnect(self) -> None:
        # Close connection
        pass
    
    async def get(self, key: str) -> Optional[Any]:
        # Retrieve data
        pass
    
    async def put(self, key: str, value: Any) -> None:
        # Store data
        pass
    
    async def delete(self, key: str) -> None:
        # Delete data
        pass
```

### Built-in Storage Types

1. File Storage:
```python
from agentsys.plugins.storage import FileStorage

storage = FileStorage(
    config=StorageConfig(
        base_path="./data",
        backup_enabled=True
    )
)
```

2. Memory Storage:
```python
from agentsys.plugins.storage import MemoryStorage

storage = MemoryStorage(
    config=StorageConfig(
        max_size=1000
    )
)
```

## Custom Plugins

Creating custom plugins:

```python
from agentsys.plugins import BasePlugin, PluginConfig
from typing import Any

class CustomPluginConfig(PluginConfig):
    option1: str = "default"
    option2: int = 42

class CustomPlugin(BasePlugin):
    def __init__(self, config: CustomPluginConfig):
        self.config = config
    
    async def initialize(self) -> None:
        # Setup plugin
        pass
    
    async def process(self, input_data: Any) -> Any:
        # Process data
        pass
    
    async def cleanup(self) -> None:
        # Cleanup resources
        pass
```

## Plugin Integration

Integrating plugins with agents:

```python
class PluginEnabledAgent(TaskAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.router = AgentRouter()
        self.storage = FileStorage()
        self.custom = CustomPlugin()
    
    async def initialize(self) -> None:
        await super().initialize()
        await self.router.initialize()
        await self.storage.connect()
        await self.custom.initialize()
    
    async def _run_task(self, input_data: Any) -> Any:
        # Use plugins in task execution
        stored_data = await self.storage.get("key")
        processed = await self.custom.process(input_data)
        result = await self.router.route_task(
            "process",
            processed
        )
        return result
    
    async def cleanup(self) -> None:
        await self.custom.cleanup()
        await self.storage.disconnect()
        await self.router.cleanup()
        await super().cleanup()
```

## Best Practices

1. **Plugin Lifecycle**:
```python
class Plugin(BasePlugin):
    async def initialize(self) -> None:
        # Setup resources
        pass
    
    async def cleanup(self) -> None:
        # Clean up resources
        pass
    
    def __del__(self):
        # Backup cleanup
        pass
```

2. **Error Handling**:
```python
class Plugin(BasePlugin):
    async def process(self, data: Any) -> Any:
        try:
            result = await self._process(data)
            return result
        except PluginError as e:
            self.log.error(f"Plugin error: {e}")
            raise
        except Exception as e:
            self.log.error(f"Unexpected error: {e}")
            raise
```

3. **Configuration Management**:
```python
class PluginConfig(BaseModel):
    enabled: bool = True
    timeout: float = 30.0
    retry_count: int = 3
    
    @validator("timeout")
    def validate_timeout(cls, v):
        if v <= 0:
            raise ValueError("Timeout must be positive")
        return v
```

4. **Resource Management**:
```python
async with Plugin(config) as plugin:
    result = await plugin.process(data)
```

5. **Monitoring and Logging**:
```python
class Plugin(BasePlugin):
    def __init__(self, config: PluginConfig):
        self.metrics = MetricsCollector()
        self.log = Logger(__name__)
    
    async def process(self, data: Any) -> Any:
        with self.metrics.measure("process_time"):
            self.log.info("Processing data")
            result = await self._process(data)
            self.log.info("Processing complete")
            return result
