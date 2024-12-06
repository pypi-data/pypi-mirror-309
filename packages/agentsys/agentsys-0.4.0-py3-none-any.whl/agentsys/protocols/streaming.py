from typing import Dict, Any, Optional, List, AsyncIterator, Callable, TypeVar, Generic
from pydantic import BaseModel, Field
import asyncio
import logging
from datetime import datetime
from enum import Enum
import json

logger = logging.getLogger(__name__)

T = TypeVar('T')

class StreamType(str, Enum):
    DATA = "data"
    CONTROL = "control"
    ERROR = "error"
    EOF = "eof"

class StreamEvent(BaseModel, Generic[T]):
    """Represents a stream event"""
    type: StreamType
    data: Optional[T] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = {}

class StreamConfig(BaseModel):
    """Configuration for stream behavior"""
    buffer_size: int = 1000
    batch_size: Optional[int] = None
    timeout: Optional[float] = None
    retry_attempts: int = 3
    retry_delay: float = 1.0

class StreamProcessor(Generic[T]):
    """Processes stream events with transformation and filtering"""
    
    def __init__(self, config: StreamConfig = StreamConfig()):
        self.config = config
        self._transformers: List[Callable[[T], T]] = []
        self._filters: List[Callable[[T], bool]] = []
    
    def add_transformer(self, transformer: Callable[[T], T]) -> None:
        """Add a transformation function"""
        self._transformers.append(transformer)
    
    def add_filter(self, filter_func: Callable[[T], bool]) -> None:
        """Add a filter function"""
        self._filters.append(filter_func)
    
    async def process(self, data: T) -> Optional[T]:
        """Process data through transformers and filters"""
        current = data
        
        try:
            # Apply transformations
            for transformer in self._transformers:
                current = await asyncio.to_thread(transformer, current)
                if current is None:
                    return None
            
            # Apply filters
            for filter_func in self._filters:
                if not await asyncio.to_thread(filter_func, current):
                    return None
            
            return current
        except Exception as e:
            logger.error(f"Error processing stream data: {str(e)}")
            return None

class StreamProducer(Generic[T]):
    """Produces stream events"""
    
    def __init__(self, config: StreamConfig = StreamConfig()):
        self.config = config
        self._queue: asyncio.Queue[StreamEvent[T]] = asyncio.Queue(maxsize=config.buffer_size)
        self._active = False
        self._processor = StreamProcessor[T](config)
    
    async def start(self) -> None:
        """Start the producer"""
        self._active = True
    
    async def stop(self) -> None:
        """Stop the producer"""
        self._active = False
        await self._queue.put(StreamEvent(type=StreamType.EOF))
    
    async def send(self, data: T, metadata: Dict[str, Any] = None) -> None:
        """Send data to the stream"""
        if not self._active:
            raise RuntimeError("Producer is not active")
        
        processed_data = await self._processor.process(data)
        if processed_data is not None:
            await self._queue.put(StreamEvent(
                type=StreamType.DATA,
                data=processed_data,
                metadata=metadata or {}
            ))
    
    async def get_stream(self) -> AsyncIterator[StreamEvent[T]]:
        """Get stream of events"""
        while self._active:
            try:
                event = await self._queue.get()
                if event.type == StreamType.EOF:
                    break
                yield event
                self._queue.task_done()
            except Exception as e:
                logger.error(f"Error in stream: {str(e)}")
                await self._queue.put(StreamEvent(
                    type=StreamType.ERROR,
                    metadata={"error": str(e)}
                ))

class StreamConsumer(Generic[T]):
    """Consumes stream events"""
    
    def __init__(self, config: StreamConfig = StreamConfig()):
        self.config = config
        self._processor = StreamProcessor[T](config)
        self._handlers: Dict[StreamType, List[Callable[[StreamEvent[T]], None]]] = {
            type_: [] for type_ in StreamType
        }
    
    def add_handler(
        self,
        event_type: StreamType,
        handler: Callable[[StreamEvent[T]], None]
    ) -> None:
        """Add an event handler"""
        self._handlers[event_type].append(handler)
    
    async def process_stream(self, stream: AsyncIterator[StreamEvent[T]]) -> None:
        """Process events from a stream"""
        batch: List[StreamEvent[T]] = []
        
        async for event in stream:
            try:
                if self.config.batch_size and len(batch) >= self.config.batch_size:
                    await self._process_batch(batch)
                    batch = []
                
                if event.type == StreamType.DATA and event.data is not None:
                    processed_data = await self._processor.process(event.data)
                    if processed_data is not None:
                        event.data = processed_data
                        batch.append(event)
                else:
                    await self._handle_event(event)
                
            except Exception as e:
                logger.error(f"Error processing stream event: {str(e)}")
                await self._handle_event(StreamEvent(
                    type=StreamType.ERROR,
                    metadata={"error": str(e)}
                ))
        
        if batch:
            await self._process_batch(batch)
    
    async def _process_batch(self, batch: List[StreamEvent[T]]) -> None:
        """Process a batch of events"""
        for event in batch:
            await self._handle_event(event)
    
    async def _handle_event(self, event: StreamEvent[T]) -> None:
        """Handle a single event"""
        for handler in self._handlers[event.type]:
            try:
                await asyncio.to_thread(handler, event)
            except Exception as e:
                logger.error(f"Error in event handler: {str(e)}")

class StreamPipeline(Generic[T]):
    """Connects producers and consumers in a pipeline"""
    
    def __init__(self, config: StreamConfig = StreamConfig()):
        self.config = config
        self.producer = StreamProducer[T](config)
        self.consumer = StreamConsumer[T](config)
    
    async def start(self) -> None:
        """Start the pipeline"""
        await self.producer.start()
        asyncio.create_task(self._run_pipeline())
    
    async def stop(self) -> None:
        """Stop the pipeline"""
        await self.producer.stop()
    
    async def _run_pipeline(self) -> None:
        """Run the pipeline"""
        try:
            await self.consumer.process_stream(self.producer.get_stream())
        except Exception as e:
            logger.error(f"Error in stream pipeline: {str(e)}")
            await self.stop()