import pytest
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional, List
from protocols.streaming import (
    StreamType,
    StreamEvent,
    StreamConfig,
    StreamPipeline,
    StreamProducer,
    StreamConsumer
)
from pydantic import BaseModel

class TestData(BaseModel):
    value: str
    timestamp: datetime = datetime.utcnow()

@pytest.fixture
def stream_config():
    return StreamConfig(buffer_size=10)

@pytest.fixture
def stream_pipeline(stream_config):
    return StreamPipeline[TestData](stream_config)

class TestStreamProtocols:
    @pytest.mark.asyncio
    async def test_stream_event_creation(self):
        data = TestData(value="test")
        event = StreamEvent[TestData](
            type=StreamType.DATA,
            data=data
        )
        assert event.type == StreamType.DATA
        assert event.data.value == "test"

    @pytest.mark.asyncio
    async def test_stream_producer(self, stream_config):
        producer = StreamProducer[TestData](stream_config)
        producer.start()
        
        data = TestData(value="test")
        await producer.send(data)
        
        async for event in producer.get_stream():
            assert event.type == StreamType.DATA
            assert event.data.value == "test"
            break
        
        producer.stop()

    @pytest.mark.asyncio
    async def test_stream_consumer(self, stream_config):
        consumer = StreamConsumer[TestData](stream_config)
        received_events = []
        
        def handler(event: StreamEvent[TestData]):
            received_events.append(event)
        
        consumer.add_handler(StreamType.DATA, handler)
        
        # Create a test stream
        async def test_stream():
            data = TestData(value="test")
            yield StreamEvent[TestData](type=StreamType.DATA, data=data)
        
        await consumer.process_stream(test_stream())
        assert len(received_events) == 1
        assert received_events[0].data.value == "test"

    @pytest.mark.asyncio
    async def test_stream_pipeline(self, stream_pipeline):
        received_events = []
        
        def handler(event: StreamEvent[TestData]):
            received_events.append(event)
        
        stream_pipeline.consumer.add_handler(StreamType.DATA, handler)
        stream_pipeline.start()
        
        data = TestData(value="test")
        await stream_pipeline.producer.send(data)
        
        # Give some time for processing
        await asyncio.sleep(0.1)
        
        assert len(received_events) == 1
        assert received_events[0].data.value == "test"
        
        stream_pipeline.stop()