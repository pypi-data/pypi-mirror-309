"""
Test script to debug imports.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

print("Python path:")
for p in sys.path:
    print(f"  {p}")

print("\nTrying imports...")
try:
    import agentsys
    print("✓ agentsys imported successfully")
    print(f"  agentsys.__file__ = {agentsys.__file__}")
except ImportError as e:
    print(f"✗ Failed to import agentsys: {e}")

try:
    from agentsys.core import BaseAgent, TaskAgent, AgentConfig
    print("✓ agentsys.core imports successful")
except ImportError as e:
    print(f"✗ Failed to import from agentsys.core: {e}")

try:
    from agentsys.core.agent import BaseAgent, TaskAgent, AgentConfig
    print("✓ agentsys.core.agent imports successful")
except ImportError as e:
    print(f"✗ Failed to import from agentsys.core.agent: {e}")

try:
    from examples.agents.multi_agent import MathAgent, CalculatorAgent, FormatAgent
    print("✓ multi_agent imports successful")
except ImportError as e:
    print(f"✗ Failed to import from multi_agent: {e}")
