# Protocols Documentation

## Overview

AgentSys protocols define communication patterns:
- Messaging: Inter-agent communication
- Streaming: Real-time data handling
- Custom protocols: Extend communication

## Messaging Protocol

Enables structured communication between agents.

```python
from agentsys.protocols.messaging import Message, MessageType, MessageBus
from typing import Any

# Define a message
message = Message(
    type=MessageType.TASK_REQUEST,
    sender="agent1",
    recipients=["agent2"],
    content={"task": "process_data", "data": {...}},
    metadata={"priority": "high"}
)

# Set up message bus
message_bus = MessageBus()

# Subscribe to message types
async def handle_task_request(message: Message):
    # Handle task request
    print(f"Received task request from {message.sender}")
    # Process the task...

message_bus.subscribe_to_commands(MessageType.TASK_REQUEST, handle_task_request)

# Start the message bus
await message_bus.start()

# Send a message
await message_bus.send_message(message)

# Stop the message bus when done
await message_bus.stop()
```

### Message Types

The following message types are supported:

```python
class MessageType(str, Enum):
    COMMAND = "command"         # Command messages
    EVENT = "event"            # Event notifications
    TASK_REQUEST = "task_request"   # Task requests
    TASK_RESPONSE = "task_response" # Task responses
    ERROR = "error"            # Error messages
```

## Streaming Protocol

Enables real-time data streaming between components.

```python
from agentsys.protocols.streaming import StreamPipeline, StreamConfig, StreamEvent

# Configure the stream
config = StreamConfig(
    buffer_size=1000,
    batch_size=100,
    flush_interval=1.0
)

# Create a pipeline
pipeline = StreamPipeline[bytes](config)

# Start streaming
await pipeline.start()

# Produce data
await pipeline.producer.send(StreamEvent(
    data=b"raw data",
    metadata={"source": "sensor1"}
))

# Consume data
async for event in pipeline.consumer:
    # Process the stream event
    print(f"Received: {event.data}, metadata: {event.metadata}")

# Stop streaming
await pipeline.stop()
```

## Custom Protocols

You can extend the base Protocol class to implement custom protocols:

```python
from agentsys.protocols.base import Protocol
from typing import Any

class CustomProtocol(Protocol):
    async def initialize(self) -> None:
        # Set up protocol resources
        pass
        
    async def send(self, data: Any) -> None:
        # Implement send logic
        pass
        
    async def receive(self) -> Any:
        # Implement receive logic
        pass
        
    async def cleanup(self) -> None:
        # Clean up resources
        pass
```

## Error Handling

All protocols include built-in error handling and logging:

```python
try:
    await protocol.send(data)
except ConnectionError:
    logger.error("Failed to send data")
    # Implement retry or fallback logic
```

## Best Practices

1. Always properly initialize and cleanup protocols
2. Use appropriate message types for different scenarios
3. Handle errors gracefully with proper logging
4. Configure buffer sizes based on your use case
5. Use metadata to add context to messages
6. Implement proper error handling and recovery
7. Monitor protocol performance with telemetry

## Protocol Integration

Integrating protocols with agents:

```python
class MultiProtocolAgent(TaskAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.messaging = MessageBus()
        self.streaming = StreamPipeline[bytes](StreamConfig())
        self.custom = CustomProtocol()
    
    async def initialize(self) -> None:
        await super().initialize()
        # Setup protocols
        await self.messaging.start()
        await self.streaming.start()
        await self.custom.initialize()
    
    async def _run_task(self, input_data: Any) -> Any:
        # Use multiple protocols
        await self.messaging.send_message(
            Message(
                type=MessageType.TASK_REQUEST,
                sender="agent1",
                recipients=["agent2"],
                content={"task": "process_data", "data": input_data},
                metadata={"priority": "high"}
            )
        )
        
        async for event in self.streaming.consumer:
            processed = await self._process(event.data)
            await self.custom.send(processed)
        
        return await self.messaging.receive()
```

## Protocol Design

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

## Flow Control

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

## Monitoring

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

## Validation

```python
class Protocol(BaseProtocol):
    async def send(self, data: Any) -> None:
        if not self.validate(data):
            raise ValueError("Invalid data")
        await self._send(data)
    
    def validate(self, data: Any) -> bool:
        # Implement validation logic
        return True
