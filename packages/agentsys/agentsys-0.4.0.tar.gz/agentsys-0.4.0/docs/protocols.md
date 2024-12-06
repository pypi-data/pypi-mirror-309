# Protocols Documentation

## Overview

AgentSys protocols define communication patterns:
- Messaging: Inter-agent communication
- Streaming: Real-time data handling
- Custom protocols: Extend communication

## Messaging Protocol

Enables structured communication between agents.

```python
from agentsys.protocols.messaging import Message, MessageProtocol
from typing import Any

class CustomMessage(Message):
    content: Any
    metadata: dict = {}
    priority: int = 0

class AgentMessaging(MessageProtocol):
    async def send(self, message: Message) -> None:
        # Send message to recipient
        await self._deliver(message)
    
    async def receive(self) -> Message:
        # Receive next message
        return await self._get_next()
    
    async def _deliver(self, message: Message) -> None:
        # Implement delivery logic
        pass
    
    async def _get_next(self) -> Message:
        # Implement message retrieval
        pass
```

### Message Types

1. Task Message:
```python
class TaskMessage(Message):
    task_id: str
    task_type: str
    payload: Any
    priority: int = 0
```

2. Control Message:
```python
class ControlMessage(Message):
    command: str
    parameters: dict = {}
    urgent: bool = False
```

3. Status Message:
```python
class StatusMessage(Message):
    status: str
    details: dict = {}
    timestamp: datetime
```

## Streaming Protocol

Handles real-time data streams.

```python
from agentsys.protocols.streaming import Stream, StreamProtocol
from typing import AsyncIterator

class DataStream(Stream):
    async def read(self) -> AsyncIterator[Any]:
        while True:
            data = await self._get_next()
            if not data:
                break
            yield data
    
    async def write(self, data: Any) -> None:
        await self._send(data)

class StreamingAgent(TaskAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stream = DataStream()
    
    async def process_stream(self) -> None:
        async for data in self.stream.read():
            processed = await self._process(data)
            await self.stream.write(processed)
```

### Stream Types

1. Event Stream:
```python
class EventStream(Stream):
    async def subscribe(self, event_type: str) -> None:
        await self._subscribe(event_type)
    
    async def publish(self, event: Any) -> None:
        await self._publish(event)
```

2. Batch Stream:
```python
class BatchStream(Stream):
    def __init__(self, batch_size: int = 100):
        self.batch_size = batch_size
    
    async def read_batch(self) -> List[Any]:
        return await self._get_batch()
    
    async def write_batch(self, batch: List[Any]) -> None:
        await self._send_batch(batch)
```

## Custom Protocols

Creating custom protocols:

```python
from agentsys.protocols import BaseProtocol, ProtocolConfig
from typing import Any

class CustomProtocolConfig(ProtocolConfig):
    buffer_size: int = 1000
    timeout: float = 30.0

class CustomProtocol(BaseProtocol):
    def __init__(self, config: CustomProtocolConfig):
        self.config = config
        self.buffer = []
    
    async def send(self, data: Any) -> None:
        # Implement send logic
        pass
    
    async def receive(self) -> Any:
        # Implement receive logic
        pass
```

## Protocol Integration

Integrating protocols with agents:

```python
class MultiProtocolAgent(TaskAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.messaging = AgentMessaging()
        self.streaming = DataStream()
        self.custom = CustomProtocol()
    
    async def initialize(self) -> None:
        await super().initialize()
        # Setup protocols
        await self.messaging.connect()
        await self.streaming.open()
        await self.custom.initialize()
    
    async def _run_task(self, input_data: Any) -> Any:
        # Use multiple protocols
        await self.messaging.send(
            TaskMessage(
                task_id="123",
                task_type="process",
                payload=input_data
            )
        )
        
        async for data in self.streaming.read():
            processed = await self._process(data)
            await self.custom.send(processed)
        
        return await self.messaging.receive()
```

## Best Practices

1. **Protocol Design**:
```python
class Protocol(BaseProtocol):
    # Clear interface
    async def send(self, data: Any) -> None:
        """Send data through the protocol."""
        pass
    
    async def receive(self) -> Any:
        """Receive data from the protocol."""
        pass
    
    # Resource management
    async def __aenter__(self):
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        await self.disconnect()
```

2. **Error Handling**:
```python
class Protocol(BaseProtocol):
    async def send(self, data: Any) -> None:
        try:
            await self._send(data)
        except ConnectionError:
            await self.reconnect()
            await self._send(data)
        except Exception as e:
            self.log.error(f"Send error: {e}")
            raise
```

3. **Flow Control**:
```python
class Protocol(BaseProtocol):
    def __init__(self, config: ProtocolConfig):
        self.buffer = asyncio.Queue(
            maxsize=config.buffer_size
        )
    
    async def send(self, data: Any) -> None:
        await self.buffer.put(data)
        if self.buffer.qsize() >= self.buffer.maxsize:
            await self._flush()
```

4. **Monitoring**:
```python
class Protocol(BaseProtocol):
    async def send(self, data: Any) -> None:
        start = time.time()
        try:
            await self._send(data)
        finally:
            duration = time.time() - start
            self.metrics.record(
                "send_duration",
                duration
            )
```

5. **Validation**:
```python
class Protocol(BaseProtocol):
    async def send(self, data: Any) -> None:
        if not self.validate(data):
            raise ValueError("Invalid data")
        await self._send(data)
    
    def validate(self, data: Any) -> bool:
        # Implement validation logic
        return True
```
