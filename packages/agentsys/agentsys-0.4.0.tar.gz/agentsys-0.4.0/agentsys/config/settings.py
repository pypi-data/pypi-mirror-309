import os
from pathlib import Path
from .base import Config

# Default configuration file path
DEFAULT_CONFIG_PATH = os.path.join(
    Path.home(),
    '.agentsys',
    'config.yaml'
)

# Default configuration
DEFAULT_CONFIG = {
    'system': {
        'debug': False,
        'log_level': 'INFO',
        'max_concurrent_agents': 10,
        'data_dir': os.path.join(Path.home(), '.agentsys', 'data'),
    },
    'agent': {
        'model': 'gpt-4',
        'temperature': 0.7,
        'max_tokens': None,
        'timeout': 60.0,
        'retry_attempts': 3,
        'cache_ttl': 3600,
    },
    'middleware': {
        'cache_enabled': True,
        'cache_size': 1000,
        'retry_enabled': True,
        'telemetry_enabled': True,
        'telemetry_flush_interval': 60.0,
    },
    'storage': {
        'storage_type': 'file',
        'storage_path': os.path.join(Path.home(), '.agentsys', 'data', 'storage'),
        'backup_enabled': True,
        'flush_interval': 60.0,
    },
    'messaging': {
        'broker_type': 'local',
        'queue_size': 1000,
        'message_ttl': 3600,
    },
}

def load_config() -> Config:
    """Load configuration from file or create default"""
    if os.path.exists(DEFAULT_CONFIG_PATH):
        return Config.load_from_file(DEFAULT_CONFIG_PATH)
    
    # Create default configuration
    config = Config(**DEFAULT_CONFIG)
    
    # Ensure config directory exists
    os.makedirs(os.path.dirname(DEFAULT_CONFIG_PATH), exist_ok=True)
    
    # Save default configuration
    with open(DEFAULT_CONFIG_PATH, 'w') as f:
        import yaml
        yaml.dump(DEFAULT_CONFIG, f, default_flow_style=False)
    
    return config

# Global configuration instance
config = load_config()