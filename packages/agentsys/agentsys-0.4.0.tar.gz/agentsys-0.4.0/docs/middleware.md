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

cache = CacheMiddleware(
    config=CacheConfig(
        max_size=1000,
        ttl_seconds=3600
    )
)

class CachedAgent(TaskAgent):
    async def _run_task(self, input_data: Any) -> Any:
        # Check cache first
        cache_key = f"{self.name}:{input_data}"
        cached = await cache.get(cache_key)
        if cached:
            return cached
        
        # Run task if not cached
        result = await super()._run_task(input_data)
        
        # Store in cache
        await cache.set(cache_key, result)
        return result
```

## Retry Middleware

Automatically retries failed operations.

```python
from agentsys.middleware import RetryMiddleware, RetryConfig

retry = RetryMiddleware(
    config=RetryConfig(
        max_retries=3,
        delay_seconds=1,
        backoff_factor=2
    )
)

class RetryingAgent(TaskAgent):
    async def execute(self, input_data: Any) -> Any:
        return await retry.run(
            func=super().execute,
            args=(input_data,)
        )
```

## Telemetry Middleware

Collects performance metrics and events.

```python
from agentsys.middleware import TelemetryMiddleware, TelemetryConfig

telemetry = TelemetryMiddleware(
    config=TelemetryConfig(
        enabled=True,
        export_interval=60
    )
)

class MonitoredAgent(TaskAgent):
    async def _run_task(self, input_data: Any) -> Any:
        with telemetry.measure(f"{self.name}_task"):
            result = await super()._run_task(input_data)
            
        telemetry.record_metric(
            name=f"{self.name}_success",
            value=1
        )
        
        return result
```

## Custom Middleware

Creating custom middleware:

```python
from agentsys.middleware import BaseMiddleware, MiddlewareConfig
from typing import Any, Callable, Awaitable

class CustomConfig(MiddlewareConfig):
    custom_option: str = "default"

class CustomMiddleware(BaseMiddleware):
    def __init__(self, config: CustomConfig):
        self.config = config
    
    async def before_execute(self, agent: 'TaskAgent', 
                           input_data: Any) -> Any:
        # Pre-processing
        return input_data
    
    async def after_execute(self, agent: 'TaskAgent',
                          result: Any) -> Any:
        # Post-processing
        return result
    
    async def on_error(self, agent: 'TaskAgent',
                      error: Exception) -> None:
        # Error handling
        pass
```

## Middleware Composition

Combining multiple middleware:

```python
class EnhancedAgent(TaskAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cache = CacheMiddleware()
        self.retry = RetryMiddleware()
        self.telemetry = TelemetryMiddleware()
    
    async def execute(self, input_data: Any) -> Any:
        # Apply middleware in sequence
        try:
            # Check cache
            cache_key = f"{self.name}:{input_data}"
            cached = await self.cache.get(cache_key)
            if cached:
                return cached
            
            # Execute with retry
            result = await self.retry.run(
                super().execute,
                args=(input_data,)
            )
            
            # Cache result
            await self.cache.set(cache_key, result)
            
            # Record metrics
            self.telemetry.record_metric(
                f"{self.name}_success",
                1
            )
            
            return result
            
        except Exception as e:
            self.telemetry.record_metric(
                f"{self.name}_error",
                1
            )
            raise e
```

## Best Practices

1. **Order Matters**: Apply middleware in a logical order:
   - Cache first (avoid unnecessary processing)
   - Retry next (handle transient failures)
   - Telemetry last (measure actual performance)

2. **Configuration**: Use appropriate settings:
```python
cache_config = CacheConfig(
    max_size=1000,      # Based on memory availability
    ttl_seconds=3600    # Based on data freshness needs
)

retry_config = RetryConfig(
    max_retries=3,      # Based on operation reliability
    delay_seconds=1,    # Based on operation timing
    backoff_factor=2    # Prevent overwhelming services
)

telemetry_config = TelemetryConfig(
    enabled=True,
    export_interval=60, # Based on monitoring needs
    batch_size=100     # Based on metric volume
)
```

3. **Resource Management**: Clean up middleware resources:
```python
async def cleanup(self):
    await self.cache.clear()
    await self.telemetry.flush()
    await super().cleanup()
```

4. **Error Handling**: Handle middleware errors appropriately:
```python
try:
    result = await self.middleware.process(input_data)
except MiddlewareError as e:
    # Handle middleware-specific errors
    self.log.error(f"Middleware error: {e}")
    raise
except Exception as e:
    # Handle other errors
    self.log.error(f"Unexpected error: {e}")
    raise
```
