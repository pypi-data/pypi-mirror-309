# Plugins Documentation

## Overview

AgentSys plugins extend the framework's functionality:
- Router: Agent communication and task routing
- Storage: Custom storage backends
- Custom plugins: Extend functionality

## Plugin System

The plugin system is built on a simple, extensible architecture:

```python
from agentsys.plugins.base import BasePlugin, PluginConfig
from typing import Any, Optional

class CustomPluginConfig(PluginConfig):
    """Plugin configuration"""
    enabled: bool = True
    name: str = "custom_plugin"
    timeout: float = 30.0

class CustomPlugin(BasePlugin):
    """Custom plugin implementation"""
    
    def __init__(self, config: CustomPluginConfig = CustomPluginConfig()):
        self.config = config
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize plugin resources"""
        if self._initialized:
            return
            
        # Setup resources
        self._initialized = True
    
    async def process(self, data: Any) -> Any:
        """Process data through plugin"""
        if not self._initialized:
            await self.initialize()
            
        # Process data
        return processed_data
    
    async def cleanup(self) -> None:
        """Clean up plugin resources"""
        if not self._initialized:
            return
            
        # Cleanup resources
        self._initialized = False
```

## Router Plugin

The Router plugin enables dynamic task routing between agents:

```python
from agentsys.plugins.router import AgentRouter, RoutingConfig, Route
from typing import List, Dict, Any

# Configure router
config = RoutingConfig(
    max_concurrent=10,
    timeout=30.0,
    retry_count=3
)

# Create router
router = AgentRouter(config)

# Define routes
@router.route("process_data")
async def process_data_route(data: Any) -> Any:
    # Create processing agent
    agent = ProcessingAgent(
        name="processor",
        description="Process data"
    )
    
    # Execute agent
    return await agent.execute(data)

@router.route("analyze_data")
async def analyze_data_route(data: Any) -> Any:
    # Create analysis agent
    agent = AnalysisAgent(
        name="analyzer",
        description="Analyze data"
    )
    
    # Execute agent
    return await agent.execute(data)

# Start router
await router.start()

# Route tasks
result = await router.route_task(
    task_name="process_data",
    task_data={"data": "raw_data"}
)

# Stop router
await router.stop()
```

## Storage Plugin

The Storage plugin provides persistent storage capabilities:

```python
from agentsys.plugins.storage import StoragePlugin, StorageConfig
from typing import Any, Optional

# Configure storage
config = StorageConfig(
    storage_type="file",
    storage_path="./storage",
    backup_enabled=True,
    flush_interval=60.0
)

# Create storage plugin
storage = StoragePlugin(config)

# Use storage
class PersistentAgent(TaskAgent):
    """Agent that uses storage"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage = storage
    
    async def initialize(self) -> None:
        await super().initialize()
        await self.storage.initialize()
    
    async def _run_task(self, input_data: Any) -> Any:
        # Store input
        key = f"task_{self.id}"
        await self.storage.store(key, input_data)
        
        # Process data
        result = await super()._run_task(input_data)
        
        # Store result
        await self.storage.store(f"{key}_result", result)
        return result
    
    async def cleanup(self) -> None:
        await self.storage.cleanup()
        await super().cleanup()
```

## Creating Custom Plugins

### Step 1: Define Plugin Configuration

```python
from agentsys.plugins.base import PluginConfig
from typing import Optional

class CustomPluginConfig(PluginConfig):
    """Configuration for custom plugin"""
    enabled: bool = True
    name: str = "custom_plugin"
    param1: str = "default"
    param2: int = 42
    timeout: float = 30.0
```

### Step 2: Implement Plugin Logic

```python
from agentsys.plugins.base import BasePlugin
from typing import Any, Optional

class CustomPlugin(BasePlugin):
    """Custom plugin implementation"""
    
    def __init__(self, config: CustomPluginConfig = CustomPluginConfig()):
        self.config = config
        self._initialized = False
        self._resources = {}
    
    async def initialize(self) -> None:
        """Initialize plugin"""
        if self._initialized:
            return
        
        # Setup resources
        self._resources = {
            "connection": await self._setup_connection(),
            "cache": await self._setup_cache()
        }
        
        self._initialized = True
    
    async def process(self, data: Any) -> Any:
        """Process data"""
        if not self._initialized:
            await self.initialize()
        
        # Process using resources
        connection = self._resources["connection"]
        cache = self._resources["cache"]
        
        # Implement processing logic
        return processed_data
    
    async def cleanup(self) -> None:
        """Cleanup resources"""
        if not self._initialized:
            return
        
        # Clean up resources
        for resource in self._resources.values():
            await resource.close()
        
        self._resources.clear()
        self._initialized = False
    
    async def _setup_connection(self) -> Any:
        """Setup connection"""
        # Implement connection setup
        pass
    
    async def _setup_cache(self) -> Any:
        """Setup cache"""
        # Implement cache setup
        pass
```

### Step 3: Use Plugin in Agent

```python
from agentsys import TaskAgent
from typing import Any

class PluginAgent(TaskAgent):
    """Agent that uses custom plugin"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.plugin = CustomPlugin(
            CustomPluginConfig(
                name="my_plugin",
                param1="custom",
                param2=100
            )
        )
    
    async def initialize(self) -> None:
        await super().initialize()
        await self.plugin.initialize()
    
    async def _run_task(self, input_data: Any) -> Any:
        # Process with plugin
        processed = await self.plugin.process(input_data)
        return await super()._run_task(processed)
    
    async def cleanup(self) -> None:
        await self.plugin.cleanup()
        await super().cleanup()
```

## Best Practices

1. Plugin Design
   - Keep plugins focused and single-purpose
   - Use clear and consistent interfaces
   - Implement proper resource management

2. Configuration
   - Use type hints for configuration
   - Provide sensible defaults
   - Validate configuration values

3. Resource Management
   - Initialize resources lazily
   - Clean up resources properly
   - Handle initialization states

4. Error Handling
   - Use appropriate error types
   - Provide detailed error messages
   - Implement proper error recovery

5. Testing
   - Write unit tests for plugins
   - Test resource management
   - Test error conditions

6. Documentation
   - Document configuration options
   - Provide usage examples
   - Document error conditions

7. Integration
   - Make plugins easy to integrate
   - Provide clear integration patterns
   - Consider backward compatibility

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
    """Simple logging plugin for agent activities"""
    
    def __init__(self, config: CustomPluginConfig):
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
            route_key="process_data",
            input_data=processed
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
