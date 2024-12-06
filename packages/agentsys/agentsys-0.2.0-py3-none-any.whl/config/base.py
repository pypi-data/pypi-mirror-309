from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
import os
import yaml
import logging.config
from pathlib import Path

class AgentConfig(BaseModel):
    """Base configuration for agents"""
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    timeout: float = 60.0
    retry_attempts: int = 3
    cache_ttl: int = 3600

class MiddlewareConfig(BaseModel):
    """Configuration for middleware components"""
    cache_enabled: bool = True
    cache_size: int = 1000
    retry_enabled: bool = True
    telemetry_enabled: bool = True
    telemetry_flush_interval: float = 60.0

class StorageConfig(BaseModel):
    """Configuration for storage"""
    storage_type: str = "file"  # "file" or "memory"
    storage_path: str = "./data"
    backup_enabled: bool = True
    flush_interval: float = 60.0

class MessagingConfig(BaseModel):
    """Configuration for messaging"""
    broker_type: str = "local"  # "local" or "redis"
    queue_size: int = 1000
    message_ttl: int = 3600

class SystemConfig(BaseModel):
    """System-wide configuration"""
    debug: bool = False
    log_level: str = "INFO"
    max_concurrent_agents: int = 10
    data_dir: str = "./data"

class Config(BaseModel):
    """Global configuration"""
    system: SystemConfig = Field(default_factory=SystemConfig)
    agent: AgentConfig = Field(default_factory=AgentConfig)
    middleware: MiddlewareConfig = Field(default_factory=MiddlewareConfig)
    storage: StorageConfig = Field(default_factory=StorageConfig)
    messaging: MessagingConfig = Field(default_factory=MessagingConfig)

    @classmethod
    def load_from_file(cls, config_path: str) -> "Config":
        """Load configuration from YAML file"""
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
        return cls(**config_data)

    def setup_logging(self) -> None:
        """Configure logging based on settings"""
        logging_config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
                },
            },
            'handlers': {
                'default': {
                    'level': self.system.log_level,
                    'formatter': 'standard',
                    'class': 'logging.StreamHandler',
                },
                'file': {
                    'level': self.system.log_level,
                    'formatter': 'standard',
                    'class': 'logging.FileHandler',
                    'filename': os.path.join(self.system.data_dir, 'agentsys.log'),
                    'mode': 'a',
                },
            },
            'loggers': {
                '': {
                    'handlers': ['default', 'file'],
                    'level': self.system.log_level,
                    'propagate': True
                },
            }
        }
        logging.config.dictConfig(logging_config)

    def ensure_directories(self) -> None:
        """Ensure required directories exist"""
        directories = [
            self.system.data_dir,
            self.storage.storage_path,
            os.path.dirname(os.path.join(self.system.data_dir, 'agentsys.log'))
        ]
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)