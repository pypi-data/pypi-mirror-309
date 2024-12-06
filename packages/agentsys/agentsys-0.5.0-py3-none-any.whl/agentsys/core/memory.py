"""Memory management for agents"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field
import json
from abc import ABC, abstractmethod

class MemoryEntry(BaseModel):
    """Represents a single memory entry"""
    key: str
    value: Any
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to a JSON-serializable dictionary"""
        return {
            "key": self.key,
            "value": self.value,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryEntry':
        """Create from a dictionary"""
        data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        return cls(**data)

class BaseMemory(ABC):
    """Abstract base class for memory implementations"""
    
    @abstractmethod
    async def store(self, key: str, value: Any, **metadata) -> None:
        """Store a value in memory"""
        pass
    
    @abstractmethod
    async def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve a value from memory"""
        pass
    
    @abstractmethod
    async def clear(self) -> None:
        """Clear all memory"""
        pass

class WorkingMemory(BaseMemory):
    """Short-term memory implementation"""
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self._memory: Dict[str, MemoryEntry] = {}
    
    async def store(self, key: str, value: Any, **metadata) -> None:
        if len(self._memory) >= self.max_size:
            # Remove oldest entry
            oldest_key = min(self._memory.keys(), key=lambda k: self._memory[k].timestamp)
            self._memory.pop(oldest_key)
        
        self._memory[key] = MemoryEntry(
            key=key,
            value=value,
            metadata=metadata
        )
    
    async def retrieve(self, key: str) -> Optional[Any]:
        entry = self._memory.get(key)
        return entry.value if entry else None
    
    async def clear(self) -> None:
        self._memory.clear()

class LongTermMemory(BaseMemory):
    """Persistent memory implementation"""
    
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        self._memory: Dict[str, MemoryEntry] = {}
        self._load_memory()
    
    def _load_memory(self):
        try:
            with open(self.storage_path, 'r') as f:
                try:
                    data = json.load(f)
                    self._memory = {
                        k: MemoryEntry.from_dict(v) for k, v in data.items()
                    }
                except json.JSONDecodeError:
                    # File is corrupted, start fresh
                    self._memory = {}
        except FileNotFoundError:
            self._memory = {}
    
    def _save_memory(self):
        with open(self.storage_path, 'w') as f:
            data = {
                k: v.to_dict() for k, v in self._memory.items()
            }
            json.dump(data, f)
    
    async def store(self, key: str, value: Any, **metadata) -> None:
        self._memory[key] = MemoryEntry(
            key=key,
            value=value,
            metadata=metadata
        )
        self._save_memory()
    
    async def retrieve(self, key: str) -> Optional[Any]:
        entry = self._memory.get(key)
        return entry.value if entry else None
    
    async def clear(self) -> None:
        self._memory.clear()
        self._save_memory()

class MemoryManager:
    """Manages different types of memory for an agent"""
    
    def __init__(self, working_memory: WorkingMemory, long_term_memory: Optional[LongTermMemory] = None):
        self.working_memory = working_memory
        self.long_term_memory = long_term_memory
    
    async def store(self, key: str, value: Any, long_term: bool = False, **metadata) -> None:
        """Store a value in memory"""
        await self.working_memory.store(key, value, **metadata)
        if long_term and self.long_term_memory:
            await self.long_term_memory.store(key, value, **metadata)
    
    async def retrieve(self, key: str, long_term: bool = False) -> Optional[Any]:
        """Retrieve a value from memory"""
        value = await self.working_memory.retrieve(key)
        if value is None and long_term and self.long_term_memory:
            value = await self.long_term_memory.retrieve(key)
        return value
    
    async def clear_all(self) -> None:
        """Clear all memory"""
        await self.working_memory.clear()
        if self.long_term_memory:
            await self.long_term_memory.clear()