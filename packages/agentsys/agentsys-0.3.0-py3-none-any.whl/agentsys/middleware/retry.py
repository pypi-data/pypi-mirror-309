from typing import Type, Callable, Any, Optional, List, Dict
import asyncio
from datetime import datetime
import logging
from pydantic import BaseModel
import random

logger = logging.getLogger(__name__)

class RetryConfig(BaseModel):
    """Configuration for retry behavior"""
    max_attempts: int = 3
    base_delay: float = 1.0  # Base delay in seconds
    max_delay: float = 30.0  # Maximum delay in seconds
    exponential_base: float = 2.0
    jitter: bool = True
    retry_exceptions: List[Type[Exception]] = [Exception]

class RetryState(BaseModel):
    """Tracks the state of retry attempts"""
    attempts: int = 0
    last_attempt: Optional[datetime] = None
    last_error: Optional[str] = None
    metadata: Dict[str, Any] = {}

class RetryHandler:
    """Handles retry logic for failed operations"""
    
    def __init__(self, config: RetryConfig = RetryConfig()):
        self.config = config
        self._states: Dict[str, RetryState] = {}
    
    def _calculate_delay(self, attempt: int) -> float:
        """Calculate the delay before the next retry attempt"""
        delay = min(
            self.config.base_delay * (self.config.exponential_base ** attempt),
            self.config.max_delay
        )
        
        if self.config.jitter:
            delay = delay * (0.5 + random.random())
        
        return delay
    
    def _should_retry(self, exception: Exception, attempt: int) -> bool:
        """Determine if an operation should be retried"""
        if attempt >= self.config.max_attempts:
            return False
            
        return any(
            isinstance(exception, exc_type)
            for exc_type in self.config.retry_exceptions
        )
    
    async def execute_with_retry(
        self,
        operation_id: str,
        operation: Callable,
        *args,
        **kwargs
    ) -> Any:
        """Execute an operation with retry logic"""
        state = self._states.get(operation_id, RetryState())
        
        while state.attempts < self.config.max_attempts:
            try:
                result = await operation(*args, **kwargs)
                self._states.pop(operation_id, None)
                return result
                
            except Exception as e:
                state.attempts += 1
                state.last_attempt = datetime.utcnow()
                state.last_error = str(e)
                
                if not self._should_retry(e, state.attempts):
                    raise
                
                delay = self._calculate_delay(state.attempts)
                logger.warning(
                    f"Operation {operation_id} failed (attempt {state.attempts}/{self.config.max_attempts}). "
                    f"Retrying in {delay:.2f} seconds. Error: {str(e)}"
                )
                
                self._states[operation_id] = state
                await asyncio.sleep(delay)
        
        raise Exception(
            f"Operation {operation_id} failed after {self.config.max_attempts} attempts. "
            f"Last error: {state.last_error}"
        )

def with_retry(
    max_attempts: Optional[int] = None,
    base_delay: Optional[float] = None,
    retry_exceptions: Optional[List[Type[Exception]]] = None
):
    """Decorator for adding retry behavior to functions"""
    def decorator(func: Callable) -> Callable:
        async def wrapper(self, *args, **kwargs) -> Any:
            if not hasattr(self, '_retry_handler'):
                config = RetryConfig()
                if max_attempts is not None:
                    config.max_attempts = max_attempts
                if base_delay is not None:
                    config.base_delay = base_delay
                if retry_exceptions is not None:
                    config.retry_exceptions = retry_exceptions
                self._retry_handler = RetryHandler(config)
            
            operation_id = f"{func.__name__}_{id(args)}_{id(kwargs)}"
            return await self._retry_handler.execute_with_retry(
                operation_id,
                func,
                self,
                *args,
                **kwargs
            )
        
        return wrapper
    return decorator