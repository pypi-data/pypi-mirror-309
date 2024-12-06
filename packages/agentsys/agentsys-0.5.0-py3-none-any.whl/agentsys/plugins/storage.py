from typing import Dict, Any, Optional, TypeVar, Generic, Type
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
import os
import json
import aiofiles
import logging
import asyncio
from pathlib import Path

logger = logging.getLogger(__name__)

T = TypeVar('T')

class StorageConfig(BaseModel):
    """Configuration for storage"""
    storage_path: str = "./data"
    file_extension: str = ".json"
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

class StorageEntry(BaseModel, Generic[T]):
    """A storage entry with metadata"""
    key: str
    value: T
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    def model_dump(self, **kwargs):
        """Custom dump to handle datetime serialization"""
        data = super().model_dump(**kwargs)
        data['created_at'] = data['created_at'].isoformat()
        data['updated_at'] = data['updated_at'].isoformat()
        return data

class FileStorage:
    """Simple file-based storage system"""
    
    def __init__(self, value_type: Type[T], config: StorageConfig = StorageConfig()):
        self.value_type = value_type
        self.config = config
        self._cache: Dict[str, StorageEntry[T]] = {}
        self._dirty: Dict[str, bool] = {}
        self._flush_task: Optional[asyncio.Task] = None
        
        # Create storage directory if it doesn't exist
        os.makedirs(self.config.storage_path, exist_ok=True)
    
    def _get_file_path(self, key: str) -> str:
        """Get the file path for a key"""
        return os.path.join(
            self.config.storage_path,
            f"{key}{self.config.file_extension}"
        )
    
    async def get(self, key: str) -> Optional[T]:
        """Get a value from storage"""
        # Check cache first
        if key in self._cache:
            return self._cache[key].value
        
        # Try to load from file
        try:
            file_path = self._get_file_path(key)
            if not os.path.exists(file_path):
                return None
            
            async with aiofiles.open(file_path, 'r') as f:
                data = json.loads(await f.read())
                # Convert ISO format strings back to datetime
                if 'created_at' in data:
                    data['created_at'] = datetime.fromisoformat(data['created_at'])
                if 'updated_at' in data:
                    data['updated_at'] = datetime.fromisoformat(data['updated_at'])
                entry = StorageEntry[T](**data)
                self._cache[key] = entry
                return entry.value
        
        except Exception as e:
            logger.error(f"Error loading entry {key}: {str(e)}")
            return None
    
    async def put(self, key: str, value: T) -> None:
        """Put a value into storage"""
        try:
            entry = StorageEntry[T](
                key=key,
                value=value,
                updated_at=datetime.utcnow()
            )
            
            # Update cache and mark as dirty
            self._cache[key] = entry
            self._dirty[key] = True
            
            # Ensure the flush task is running
            if not self._flush_task or self._flush_task.done():
                self._flush_task = asyncio.create_task(self._flush_dirty())
        
        except Exception as e:
            logger.error(f"Error putting entry {key}: {str(e)}")
            raise
    
    async def delete(self, key: str) -> None:
        """Delete a value from storage"""
        try:
            # Remove from cache
            self._cache.pop(key, None)
            self._dirty.pop(key, None)
            
            # Remove file if it exists
            file_path = self._get_file_path(key)
            if os.path.exists(file_path):
                os.remove(file_path)
        
        except Exception as e:
            logger.error(f"Error deleting entry {key}: {str(e)}")
            raise
    
    async def _flush_dirty(self) -> None:
        """Flush dirty entries to disk"""
        while self._dirty:
            for key in list(self._dirty.keys()):
                try:
                    entry = self._cache[key]
                    file_path = self._get_file_path(key)
                    
                    # Ensure directory exists
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    
                    # Write to file
                    async with aiofiles.open(file_path, 'w') as f:
                        await f.write(json.dumps(entry.model_dump(), indent=2))
                    
                    self._dirty.pop(key)
                
                except Exception as e:
                    logger.error(f"Error flushing entry {key}: {str(e)}")
            
            # Wait a bit before next flush
            await asyncio.sleep(0.1)
    
    async def close(self) -> None:
        """Close the storage and flush any remaining entries"""
        if self._flush_task:
            try:
                await self._flush_task
            except Exception as e:
                logger.error(f"Error in final flush: {str(e)}")
            finally:
                self._flush_task = None