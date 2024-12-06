import pytest
import asyncio
import json
from datetime import datetime, timedelta
from middleware.cache import ResponseCache, CacheConfig
from middleware.retry import RetryHandler, RetryConfig
from middleware.telemetry import (
    TelemetryCollector,
    TelemetryConfig,
    MetricType,
    LogLevel,
    TelemetryMiddleware, 
    Event,
    MetricPoint
)

@pytest.fixture
def cache():
    return ResponseCache(CacheConfig(ttl=60))

@pytest.fixture
def retry_handler():
    return RetryHandler(RetryConfig(max_attempts=3))

@pytest.fixture
def telemetry_collector():
    return TelemetryCollector(TelemetryConfig())

@pytest.fixture
def telemetry():
    config = TelemetryConfig(
        enabled=True,
        log_metrics=False,
        log_events=False
    )
    return TelemetryMiddleware(config)

class TestCache:
    @pytest.mark.asyncio
    async def test_cache_set_get(self, cache):
        key = "test_key"
        value = "test_value"
        
        await cache.set(key, value)
        result = await cache.get(key)
        
        assert result == value
    
    @pytest.mark.asyncio
    async def test_cache_expiration(self, cache):
        key = "test_key"
        value = "test_value"
        
        # Set with short TTL
        cache.config.ttl = 1
        await cache.set(key, value)
        
        # Verify value exists
        result = await cache.get(key)
        assert result == value
        
        # Wait for expiration
        await asyncio.sleep(1.1)
        
        # Value should be gone
        result = await cache.get(key)
        assert result is None
    
    @pytest.mark.asyncio
    async def test_cache_max_size(self, cache):
        cache.config.max_size = 2
        
        # Add three items
        await cache.set("key1", "value1")
        await cache.set("key2", "value2")
        await cache.set("key3", "value3")
        
        # First item should be evicted
        assert await cache.get("key1") is None
        assert await cache.get("key2") is not None
        assert await cache.get("key3") is not None

class TestRetry:
    @pytest.mark.asyncio
    async def test_successful_operation(self, retry_handler):
        async def operation():
            return "success"
        
        result = await retry_handler.execute_with_retry(
            "test_op",
            operation
        )
        assert result == "success"
    
    @pytest.mark.asyncio
    async def test_retry_on_failure(self, retry_handler):
        attempts = 0
        
        async def failing_operation():
            nonlocal attempts
            attempts += 1
            if attempts < 3:
                raise ValueError("Test error")
            return "success"
        
        result = await retry_handler.execute_with_retry(
            "test_op",
            failing_operation
        )
        
        assert result == "success"
        assert attempts == 3
    
    @pytest.mark.asyncio
    async def test_max_retries_exceeded(self, retry_handler):
        async def always_fails():
            raise ValueError("Test error")
        
        with pytest.raises(Exception):
            await retry_handler.execute_with_retry(
                "test_op",
                always_fails
            )

class TestTelemetry:
    @pytest.mark.asyncio
    async def test_metric_recording(self, telemetry_collector):
        await telemetry_collector.record_metric(
            "test_metric",
            1.0,
            MetricType.GAUGE
        )
        
        # Metrics should be in the internal list
        assert len(telemetry_collector._metrics) == 1
        assert telemetry_collector._metrics[0].name == "test_metric"
    
    @pytest.mark.asyncio
    async def test_event_recording(self, telemetry_collector):
        await telemetry_collector.record_event(
            "test_event",
            {"key": "value"},
            LogLevel.INFO
        )
        
        # Event should be in the internal list
        assert len(telemetry_collector._events) == 1
        assert telemetry_collector._events[0].name == "test_event"
    
    @pytest.mark.asyncio
    async def test_metric_handlers(self, telemetry_collector):
        handled_metrics = []
        
        async def metric_handler(metric):
            handled_metrics.append(metric)
        
        telemetry_collector.add_handler("metric", metric_handler)
        await telemetry_collector.record_metric("test_metric", 1.0)
        
        assert len(handled_metrics) == 1
    
    @pytest.mark.asyncio
    async def test_flush_operation(self, telemetry_collector):
        # Record some data
        await telemetry_collector.record_metric("test_metric", 1.0)
        await telemetry_collector.record_event("test_event", {})
        
        # Flush
        await telemetry_collector.flush()
        
        # Internal buffers should be empty
        assert len(telemetry_collector._metrics) == 0
        assert len(telemetry_collector._events) == 0
    
    @pytest.mark.asyncio
    async def test_telemetry_disabled(self, telemetry_collector):
        telemetry_collector.config.enabled = False
        
        await telemetry_collector.record_metric("test_metric", 1.0)
        await telemetry_collector.record_event("test_event", {})
        
        assert len(telemetry_collector._metrics) == 0
        assert len(telemetry_collector._events) == 0

class TestTelemetryMiddleware:
    def test_metric_recording(self, telemetry):
        telemetry.record_metric("test_metric", 42.0, MetricType.COUNTER)
        assert len(telemetry._metrics) == 1
        metric = telemetry._metrics[0]
        assert isinstance(metric, MetricPoint)
        assert metric.name == "test_metric"
        assert metric.value == 42.0
        assert metric.type == MetricType.COUNTER
        assert isinstance(metric.timestamp, datetime)

    def test_event_recording(self, telemetry):
        telemetry.record_event("test_event", {"key": "value"}, "info")
        assert len(telemetry._events) == 1
        event = telemetry._events[0]
        assert isinstance(event, Event)
        assert event.name == "test_event"
        assert event.data == {"key": "value"}
        assert event.severity == "info"
        assert isinstance(event.timestamp, datetime)

    @pytest.mark.asyncio
    async def test_telemetry_export(self, tmp_path, telemetry):
        export_file = tmp_path / "telemetry.json"
        telemetry.config.export_path = str(export_file)
        
        telemetry.record_metric("test_metric", 42.0, MetricType.GAUGE)
        telemetry.record_event("test_event", {"key": "value"})
        
        await telemetry.export_telemetry()
        
        assert export_file.exists()
        with open(export_file) as f:
            data = json.load(f)
            assert "metrics" in data
            assert "events" in data
            assert len(data["metrics"]) == 1
            assert len(data["events"]) == 1

    @pytest.mark.asyncio
    async def test_telemetry_decorator(self, telemetry):
        @telemetry.with_telemetry("test_function")
        async def test_func():
            return "success"
        
        result = await test_func()
        assert result == "success"
        assert len(telemetry._events) == 1
        event = telemetry._events[0]
        assert event.name == "test_function.success"
        assert "duration" in event.data

    @pytest.mark.asyncio
    async def test_telemetry_decorator_error(self, telemetry):
        @telemetry.with_telemetry("test_function")
        async def test_func():
            raise ValueError("test error")
        
        with pytest.raises(ValueError):
            await test_func()
        
        assert len(telemetry._events) == 1
        event = telemetry._events[0]
        assert event.name == "test_function.error"
        assert event.severity == "error"
        assert "error" in event.data
        assert event.data["error"] == "test error"
        assert "duration" in event.data