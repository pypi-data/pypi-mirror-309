"""
AgentSys - A robust, asynchronous multi-agent development framework
"""

__version__ = "0.3.0"

import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from agentsys.core import *
from agentsys.middleware import *
from agentsys.plugins import *
from agentsys.protocols import *
from agentsys.config import *

__all__ = ['core', 'middleware', 'plugins', 'protocols', 'config']
