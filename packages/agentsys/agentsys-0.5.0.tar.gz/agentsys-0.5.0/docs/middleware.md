# Middleware Documentation

## Overview

AgentSys middleware provides additional functionality that can be applied to agents:
- Caching responses
- Automatic retries
- Performance monitoring
- Custom middleware creation

## Cache Middleware

Caches agent responses for improved performance.

```python
from agentsys.middleware import CacheMiddleware, CacheConfig

# Configure cache
config = CacheConfig(
    max_size=1000,
    ttl_seconds=3600,
    storage_path="./cache"
)

# Create cache middleware
cache = CacheMiddleware(config)

# Use in agent
class CachedAgent(TaskAgent):
    async def initialize(self) -> None:
        await super().initialize()
        await cache.initialize()
    
    async def _run_task(self, input_data: Any) -> Any:
        # Generate cache key
        cache_key = f"{self.id}:{hash(str(input_data))}"
        
        # Try cache first
        cached = await cache.get(cache_key)
        if cached:
            return cached
        
        # Run task if not cached
        result = await super()._run_task(input_data)
        
        # Store in cache
        await cache.set(cache_key, result)
        return result
    
    async def cleanup(self) -> None:
        await cache.cleanup()
        await super().cleanup()
```

## Telemetry Middleware

Collects performance metrics and events.

```python
from agentsys.middleware import TelemetryMiddleware, TelemetryConfig
from datetime import datetime

# Configure telemetry
config = TelemetryConfig(
    enabled=True,
    flush_interval=60.0,
    export_path="./telemetry"
)

# Create telemetry middleware
telemetry = TelemetryMiddleware(config)

# Use in agent
class MonitoredAgent(TaskAgent):
    async def initialize(self) -> None:
        await super().initialize()
        await telemetry.initialize()
        
        # Record initialization
        telemetry.record_event(
            name="agent_initialized",
            agent_id=self.id,
            timestamp=datetime.utcnow()
        )
    
    async def _run_task(self, input_data: Any) -> Any:
        start_time = datetime.utcnow()
        
        try:
            result = await super()._run_task(input_data)
            
            # Record metrics
            duration = (datetime.utcnow() - start_time).total_seconds()
            telemetry.record_metric(
                name="task_duration",
                value=duration,
                agent_id=self.id
            )
            
            return result
            
        except Exception as e:
            # Record error
            telemetry.record_event(
                name="task_error",
                agent_id=self.id,
                error=str(e)
            )
            raise
    
    async def cleanup(self) -> None:
        await telemetry.flush()
        await super().cleanup()
```

## Retry Middleware

Automatically retries failed operations.

```python
from agentsys.middleware import RetryMiddleware, RetryConfig

# Configure retry behavior
config = RetryConfig(
    max_retries=3,
    delay_seconds=1.0,
    backoff_factor=2.0,
    exceptions=[ConnectionError, TimeoutError]
)

# Create retry middleware
retry = RetryMiddleware(config)

# Use in agent
class RetryAgent(TaskAgent):
    async def _run_task(self, input_data: Any) -> Any:
        @retry.retry
        async def run_with_retry():
            return await super()._run_task(input_data)
        
        return await run_with_retry()
```

## Custom Middleware

Create your own middleware:

```python
from agentsys.middleware import BaseMiddleware, MiddlewareConfig
from typing import Any, Optional

class CustomConfig(MiddlewareConfig):
    """Custom middleware configuration"""
    param1: str = "default"
    param2: int = 42

class CustomMiddleware(BaseMiddleware):
    """Custom middleware implementation"""
    
    def __init__(self, config: CustomConfig):
        self.config = config
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize middleware"""
        if self._initialized:
            return
        
        # Setup resources
        self._initialized = True
    
    async def process(self, data: Any) -> Any:
        """Process data"""
        # Implement processing logic
        return processed_data
    
    async def cleanup(self) -> None:
        """Cleanup resources"""
        if not self._initialized:
            return
        
        # Cleanup resources
        self._initialized = False

# Use custom middleware
class CustomAgent(TaskAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.middleware = CustomMiddleware(CustomConfig())
    
    async def initialize(self) -> None:
        await super().initialize()
        await self.middleware.initialize()
    
    async def _run_task(self, input_data: Any) -> Any:
        # Process with middleware
        processed = await self.middleware.process(input_data)
        return await super()._run_task(processed)
    
    async def cleanup(self) -> None:
        await self.middleware.cleanup()
        await super().cleanup()
```

## Middleware Chaining

Chain multiple middleware together:

```python
class EnhancedAgent(TaskAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Initialize middleware
        self.cache = CacheMiddleware(CacheConfig())
        self.telemetry = TelemetryMiddleware(TelemetryConfig())
        self.retry = RetryMiddleware(RetryConfig())
    
    async def initialize(self) -> None:
        await super().initialize()
        
        # Initialize all middleware
        await self.cache.initialize()
        await self.telemetry.initialize()
        await self.retry.initialize()
    
    async def _run_task(self, input_data: Any) -> Any:
        # Generate cache key
        cache_key = f"{self.id}:{hash(str(input_data))}"
        
        # Try cache first
        cached = await self.cache.get(cache_key)
        if cached:
            return cached
        
        # Run with retry and telemetry
        start_time = datetime.utcnow()
        
        @self.retry.retry
        async def run_with_retry():
            return await super()._run_task(input_data)
        
        try:
            result = await run_with_retry()
            
            # Record metrics
            duration = (datetime.utcnow() - start_time).total_seconds()
            self.telemetry.record_metric(
                name="task_duration",
                value=duration,
                agent_id=self.id
            )
            
            # Cache result
            await self.cache.set(cache_key, result)
            return result
            
        except Exception as e:
            # Record error
            self.telemetry.record_event(
                name="task_error",
                agent_id=self.id,
                error=str(e)
            )
            raise
    
    async def cleanup(self) -> None:
        # Cleanup all middleware
        await self.cache.cleanup()
        await self.telemetry.flush()
        await self.retry.cleanup()
        await super().cleanup()
```

## Best Practices

1. Always initialize middleware before use
2. Clean up middleware resources properly
3. Use appropriate configuration for your use case
4. Handle middleware errors gracefully
5. Monitor middleware performance
6. Chain middleware in a logical order
7. Keep middleware implementations simple and focused
