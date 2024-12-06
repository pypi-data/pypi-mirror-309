from typing import Type, Callable, Any, Optional, List, Dict, Union, Tuple
import asyncio
from datetime import datetime
import logging
from pydantic import BaseModel
import random
from functools import wraps

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
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]] = Exception
):
    """Decorator to retry functions on failure
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for delay after each retry
        exceptions: Exception types to retry on
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            attempt = 1
            current_delay = delay
            
            while attempt <= max_attempts:
                try:
                    return await func(*args, **kwargs)
                
                except exceptions as e:
                    if attempt == max_attempts:
                        logger.error(f"Final attempt {attempt} failed: {str(e)}")
                        raise
                    
                    logger.warning(f"Attempt {attempt} failed: {str(e)}")
                    
                    # Add some randomness to prevent thundering herd
                    jitter = random.uniform(0, 0.1 * current_delay)
                    await asyncio.sleep(current_delay + jitter)
                    
                    current_delay *= backoff
                    attempt += 1
        
        return wrapper
    return decorator