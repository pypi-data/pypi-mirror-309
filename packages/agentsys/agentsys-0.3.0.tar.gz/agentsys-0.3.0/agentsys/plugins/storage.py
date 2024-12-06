from typing import Dict, Any, Optional, List, Type, TypeVar, Generic
from pydantic import BaseModel, Field, ConfigDict
import json
import asyncio
import aiofiles
import logging
from datetime import datetime
from abc import ABC, abstractmethod
import os
import pickle

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=BaseModel)

class StorageConfig(BaseModel):
    """Configuration for storage behavior"""
    storage_path: str
    serialization_format: str = "json"  # or "pickle"
    auto_flush: bool = True
    flush_interval: float = 60.0
    create_backup: bool = True
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

class StorageEntry(BaseModel, Generic[T]):
    """Represents a stored item"""
    key: str
    value: T
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    def model_dump_json(self, **kwargs):
        """Custom JSON serialization to handle datetime"""
        def datetime_handler(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            return str(obj)
        
        return json.dumps(
            self.model_dump(),
            default=datetime_handler,
            **kwargs
        )

class BaseStorage(ABC, Generic[T]):
    """Abstract base class for storage implementations"""
    
    @abstractmethod
    async def get(self, key: str) -> Optional[T]:
        """Retrieve an item by key"""
        pass
    
    @abstractmethod
    async def put(self, key: str, value: T, metadata: Dict[str, Any] = None) -> None:
        """Store an item"""
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete an item"""
        pass
    
    @abstractmethod
    async def list(self, prefix: str = "") -> List[str]:
        """List all keys with optional prefix"""
        pass

class FileStorage(BaseStorage[T]):
    """File-based storage implementation"""
    
    def __init__(self, model_type: Type[T], config: StorageConfig):
        self.model_type = model_type
        self.config = config
        self._data: Dict[str, StorageEntry[T]] = {}
        self._lock = asyncio.Lock()
        self._flush_task: Optional[asyncio.Task] = None
        self._ensure_storage_path()
    
    def _ensure_storage_path(self) -> None:
        """Ensure storage directory exists"""
        os.makedirs(self.config.storage_path, exist_ok=True)
    
    def _get_file_path(self, key: str) -> str:
        """Get file path for a key"""
        return os.path.join(self.config.storage_path, f"{key}.json")
    
    async def _serialize(self, entry: StorageEntry[T]) -> bytes:
        """Serialize an entry"""
        try:
            if self.config.serialization_format == "json":
                return entry.model_dump_json(indent=2).encode('utf-8')
            else:
                return pickle.dumps(entry)
        except Exception as e:
            logger.error(f"Error serializing entry: {str(e)}")
            raise
    
    async def _deserialize(self, data: bytes) -> StorageEntry[T]:
        """Deserialize an entry"""
        try:
            if self.config.serialization_format == "json":
                data_dict = json.loads(data.decode('utf-8'))
                # Convert ISO format strings back to datetime
                for dt_field in ['created_at', 'updated_at']:
                    if dt_field in data_dict:
                        data_dict[dt_field] = datetime.fromisoformat(data_dict[dt_field])
                # Convert value back to model type
                if 'value' in data_dict:
                    data_dict['value'] = self.model_type(**data_dict['value'])
                return StorageEntry[T](**data_dict)
            else:
                return pickle.loads(data)
        except Exception as e:
            logger.error(f"Error deserializing data: {str(e)}")
            raise

    async def get(self, key: str) -> Optional[T]:
        """Retrieve an item by key"""
        async with self._lock:
            if key in self._data:
                return self._data[key].value
            
            try:
                file_path = self._get_file_path(key)
                async with aiofiles.open(file_path, 'rb') as f:
                    data = await f.read()
                entry = await self._deserialize(data)
                self._data[key] = entry
                return entry.value
            except FileNotFoundError:
                return None
            except Exception as e:
                logger.error(f"Error reading file {key}: {str(e)}")
                return None
    
    async def put(self, key: str, value: T, metadata: Dict[str, Any] = None) -> None:
        """Store an item"""
        logger.debug(f"Starting put operation for key: {key}")
        now = datetime.utcnow()
        entry = StorageEntry[T](
            key=key,
            value=value,
            created_at=now,
            updated_at=now,
            metadata=metadata or {}
        )
        
        async with self._lock:
            logger.debug(f"Acquired lock for key: {key}")
            self._data[key] = entry
            if self.config.auto_flush:
                logger.debug(f"Auto-flushing enabled, flushing entry: {key}")
                await self._flush_entry(key, entry)
            logger.debug(f"Put operation completed for key: {key}")

    async def delete(self, key: str) -> None:
        """Delete an item"""
        async with self._lock:
            self._data.pop(key, None)
            try:
                file_path = self._get_file_path(key)
                await asyncio.to_thread(os.remove, file_path)
            except FileNotFoundError:
                pass
    
    async def list(self, prefix: str = "") -> List[str]:
        """List all keys with optional prefix"""
        async with self._lock:
            return [key for key in self._data.keys() if key.startswith(prefix)]
    
    async def _flush_entry(self, key: str, entry: StorageEntry[T]) -> None:
        """Flush a single entry to storage"""
        try:
            file_path = self._get_file_path(key)
            logger.debug(f"Starting flush for key: {key}")
            
            # Create backup if needed
            if self.config.create_backup and os.path.exists(file_path):
                backup_path = f"{file_path}.bak"
                logger.debug(f"Creating backup at: {backup_path}")
                await asyncio.to_thread(os.rename, file_path, backup_path)
                logger.debug(f"Backup created successfully")
            
            # Serialize and write
            logger.debug(f"Serializing entry for key: {key}")
            serialized = await self._serialize(entry)
            logger.debug(f"Opening file for writing: {file_path}")
            async with aiofiles.open(file_path, 'wb') as f:
                logger.debug(f"Writing {len(serialized)} bytes")
                await f.write(serialized)
                await f.flush()
                logger.debug(f"Write completed successfully")
                
        except Exception as e:
            logger.error(f"Error flushing entry {key}: {str(e)}", exc_info=True)
            raise

    async def flush_all(self) -> None:
        """Flush all entries to storage"""
        async with self._lock:
            for key, entry in self._data.items():
                await self._flush_entry(key, entry)
    
    async def start_flush_loop(self) -> None:
        """Start periodic flushing of data"""
        if self._flush_task is None:
            self._flush_task = asyncio.create_task(self._flush_loop())
    
    async def stop_flush_loop(self) -> None:
        """Stop the flush loop"""
        if self._flush_task:
            self._flush_task.cancel()
            try:
                await self._flush_task
            except asyncio.CancelledError:
                pass
            self._flush_task = None
            await self.flush_all()
    
    async def _flush_loop(self) -> None:
        """Periodically flush data to storage"""
        while True:
            try:
                await asyncio.sleep(self.config.flush_interval)
                await self.flush_all()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in flush loop: {str(e)}")

class MemoryStorage(BaseStorage[T]):
    """In-memory storage implementation"""
    
    def __init__(self, model_type: Type[T]):
        self.model_type = model_type
        self._data: Dict[str, StorageEntry[T]] = {}
        self._lock = asyncio.Lock()
    
    async def get(self, key: str) -> Optional[T]:
        async with self._lock:
            entry = self._data.get(key)
            return entry.value if entry else None
    
    async def put(self, key: str, value: T, metadata: Dict[str, Any] = None) -> None:
        now = datetime.utcnow()
        entry = StorageEntry[T](
            key=key,
            value=value,
            created_at=now,
            updated_at=now,
            metadata=metadata or {}
        )
        async with self._lock:
            self._data[key] = entry
    
    async def delete(self, key: str) -> None:
        async with self._lock:
            self._data.pop(key, None)
    
    async def list(self, prefix: str = "") -> List[str]:
        async with self._lock:
            return [key for key in self._data.keys() if key.startswith(prefix)]