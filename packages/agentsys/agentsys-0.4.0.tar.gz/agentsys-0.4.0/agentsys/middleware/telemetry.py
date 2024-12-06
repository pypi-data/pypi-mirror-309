from typing import Dict, Any, Optional, List, Callable, Union
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from enum import Enum
import json
import logging
import asyncio
from functools import wraps
import time

logger = logging.getLogger(__name__)

def datetime_handler(obj):
    """JSON serializer for datetime objects"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

class LogLevel(str, Enum):
    """Log levels for events"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"

class MetricType(str, Enum):
    """Types of metrics that can be collected"""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"

class MetricPoint(BaseModel):
    """A single metric measurement"""
    name: str
    value: float
    type: MetricType = MetricType.GAUGE
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    labels: Dict[str, str] = Field(default_factory=dict)
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

class Event(BaseModel):
    """A telemetry event"""
    name: str
    data: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    severity: Union[str, LogLevel] = LogLevel.INFO
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

class TelemetryConfig(BaseModel):
    """Configuration for telemetry middleware"""
    enabled: bool = True
    log_metrics: bool = True
    log_events: bool = True
    export_path: Optional[str] = None
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

class TelemetryCollector:
    """Async telemetry collector with handlers"""
    def __init__(self, config: TelemetryConfig = TelemetryConfig()):
        self.config = config
        self._metrics: List[MetricPoint] = []
        self._events: List[Event] = []
        self._metric_handlers: List[Callable] = []
        self._event_handlers: List[Callable] = []
    
    def add_handler(self, type_: str, handler: Callable) -> None:
        """Add a handler for metrics or events"""
        if type_ == "metric":
            self._metric_handlers.append(handler)
        elif type_ == "event":
            self._event_handlers.append(handler)
    
    async def record_metric(
        self, 
        name: str, 
        value: float, 
        type_: MetricType = MetricType.GAUGE,
        labels: Optional[Dict[str, str]] = None
    ) -> None:
        """Record a metric asynchronously"""
        if not self.config.enabled:
            return
        
        metric = MetricPoint(
            name=name,
            value=value,
            type=type_,
            labels=labels or {}
        )
        self._metrics.append(metric)
        
        for handler in self._metric_handlers:
            await handler(metric)
        
        if self.config.log_metrics:
            logger.info(f"Metric: {name}={value} type={type_.value} {labels or ''}")
    
    async def record_event(
        self, 
        name: str, 
        data: Optional[Dict[str, Any]] = None, 
        severity: LogLevel = LogLevel.INFO
    ) -> None:
        """Record an event asynchronously"""
        if not self.config.enabled:
            return
        
        event = Event(
            name=name,
            data=data or {},
            severity=severity
        )
        self._events.append(event)
        
        for handler in self._event_handlers:
            await handler(event)
        
        if self.config.log_events:
            logger.log(
                logging.getLevelName(severity.value.upper()),
                f"Event: {name} {data or ''}"
            )
    
    async def flush(self) -> None:
        """Flush all metrics and events"""
        self._metrics.clear()
        self._events.clear()

class TelemetryMiddleware:
    """Synchronous telemetry middleware for function decoration"""
    def __init__(self, config: TelemetryConfig = TelemetryConfig()):
        self.config = config
        self._metrics: List[MetricPoint] = []
        self._events: List[Event] = []
        self._export_task: Optional[asyncio.Task] = None
    
    def record_metric(
        self, 
        name: str, 
        value: float, 
        metric_type: MetricType = MetricType.GAUGE,
        labels: Optional[Dict[str, str]] = None
    ) -> None:
        """Record a metric measurement"""
        if not self.config.enabled:
            return
        
        metric = MetricPoint(
            name=name,
            value=value,
            type=metric_type,
            labels=labels or {}
        )
        self._metrics.append(metric)
        
        if self.config.log_metrics:
            logger.info(f"Metric: {name}={value} type={metric_type.value} {labels or ''}")
    
    def record_event(self, name: str, data: Optional[Dict[str, Any]] = None, severity: str = "info") -> None:
        """Record an event"""
        if not self.config.enabled:
            return
        
        event = Event(
            name=name,
            data=data or {},
            severity=severity
        )
        self._events.append(event)
        
        if self.config.log_events:
            logger.log(
                logging.getLevelName(severity.upper()),
                f"Event: {name} {data or ''}"
            )
    
    async def export_telemetry(self) -> None:
        """Export collected telemetry data"""
        if not self.config.export_path:
            return
        
        try:
            data = {
                "metrics": [metric.model_dump() for metric in self._metrics],
                "events": [event.model_dump() for event in self._events]
            }
            
            with open(self.config.export_path, 'w') as f:
                json.dump(data, f, default=datetime_handler)
        except Exception as e:
            logger.error(f"Failed to export telemetry: {e}")
            raise
    
    def with_telemetry(self, name: str):
        """Decorator to add telemetry to a function"""
        def decorator(func: Callable):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                start_time = datetime.utcnow()
                try:
                    result = await func(*args, **kwargs)
                    self.record_event(
                        f"{name}.success",
                        {"duration": (datetime.utcnow() - start_time).total_seconds()}
                    )
                    return result
                except Exception as e:
                    self.record_event(
                        f"{name}.error",
                        {
                            "error": str(e),
                            "duration": (datetime.utcnow() - start_time).total_seconds()
                        },
                        severity="error"
                    )
                    raise
            return wrapper
        return decorator

def with_telemetry(name: Optional[str] = None):
    """Decorator to add telemetry to a function"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Use function name if no name provided
            event_name = name or func.__name__
            
            # Record start event
            start_time = time.time()
            logger.info(f"Starting {event_name}")
            
            try:
                # Execute function
                result = await func(*args, **kwargs)
                
                # Record success event
                duration = time.time() - start_time
                logger.info(f"Completed {event_name} in {duration:.2f}s")
                
                return result
            
            except Exception as e:
                # Record error event
                duration = time.time() - start_time
                logger.error(f"Error in {event_name} after {duration:.2f}s: {str(e)}")
                raise
        
        return wrapper
    return decorator