from typing import Any, Optional, Dict, Callable
from datetime import datetime, timedelta
import hashlib
import json
import asyncio
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

class CacheEntry(BaseModel):
    """Represents a cached response"""
    key: str
    value: Any
    expires_at: Optional[datetime] = None
    metadata: Dict[str, Any] = {}

class CacheConfig(BaseModel):
    """Configuration for cache behavior"""
    ttl: Optional[int] = 3600  # Time to live in seconds
    max_size: Optional[int] = 1000  # Maximum number of entries
    enabled: bool = True

class ResponseCache:
    """Implements caching for agent responses"""
    
    def __init__(self, config: CacheConfig = CacheConfig()):
        self.config = config
        self._cache: Dict[str, CacheEntry] = {}
        self._cleanup_task: Optional[asyncio.Task] = None
    
    def _generate_key(self, input_data: Any, context: Dict[str, Any] = None) -> str:
        """Generate a cache key from input data and context"""
        key_data = {
            'input': input_data,
            'context': context or {}
        }
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.sha256(key_str.encode()).hexdigest()
    
    async def get(self, key: str) -> Optional[Any]:
        """Retrieve a value from cache"""
        if not self.config.enabled:
            return None
            
        entry = self._cache.get(key)
        if entry is None:
            return None
            
        if entry.expires_at and entry.expires_at < datetime.utcnow():
            self._cache.pop(key, None)
            return None
            
        return entry.value
    
    async def set(self, key: str, value: Any, metadata: Dict[str, Any] = None) -> None:
        """Store a value in cache"""
        if not self.config.enabled:
            return
            
        if self.config.max_size and len(self._cache) >= self.config.max_size:
            # Remove oldest entry
            oldest_key = min(self._cache.keys(), 
                           key=lambda k: self._cache[k].expires_at or datetime.max)
            self._cache.pop(oldest_key)
        
        expires_at = None
        if self.config.ttl:
            expires_at = datetime.utcnow() + timedelta(seconds=self.config.ttl)
        
        self._cache[key] = CacheEntry(
            key=key,
            value=value,
            expires_at=expires_at,
            metadata=metadata or {}
        )
    
    async def invalidate(self, key: str) -> None:
        """Remove a specific entry from cache"""
        self._cache.pop(key, None)
    
    async def clear(self) -> None:
        """Clear all cached entries"""
        self._cache.clear()
    
    async def start_cleanup(self) -> None:
        """Start periodic cleanup of expired entries"""
        if self._cleanup_task is None:
            self._cleanup_task = asyncio.create_task(self._cleanup_loop())
    
    async def stop_cleanup(self) -> None:
        """Stop the cleanup task"""
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
            self._cleanup_task = None
    
    async def _cleanup_loop(self) -> None:
        """Periodically remove expired entries"""
        while True:
            try:
                now = datetime.utcnow()
                expired_keys = [
                    key for key, entry in self._cache.items()
                    if entry.expires_at and entry.expires_at < now
                ]
                for key in expired_keys:
                    self._cache.pop(key, None)
                
                await asyncio.sleep(60)  # Run cleanup every minute
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in cache cleanup: {str(e)}")
                await asyncio.sleep(60)

def cache_response(ttl: Optional[int] = None):
    """Decorator for caching agent responses"""
    def decorator(func: Callable) -> Callable:
        async def wrapper(self, *args, **kwargs) -> Any:
            if not hasattr(self, '_response_cache'):
                self._response_cache = ResponseCache(
                    CacheConfig(ttl=ttl if ttl is not None else 3600)
                )
            
            cache_key = self._response_cache._generate_key(args[0] if args else None, kwargs)
            cached_result = await self._response_cache.get(cache_key)
            
            if cached_result is not None:
                return cached_result
            
            result = await func(self, *args, **kwargs)
            await self._response_cache.set(cache_key, result)
            return result
            
        return wrapper
    return decorator