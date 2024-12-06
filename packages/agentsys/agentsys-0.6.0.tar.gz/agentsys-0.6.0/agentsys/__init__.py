"""
Swarm: A lightweight, stateless multi-agent orchestration framework.
"""

from .orchestration import Swarm
from .types import Agent, Function, Response, Result
from .config import Settings

__version__ = "0.1.0"

__all__ = [
    'Swarm',
    'Agent',
    'Function',
    'Response',
    'Result',
    'Settings',
]
