"""
Pytest configuration for tests.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Add examples directory to path
examples_dir = project_root / "examples"
if str(examples_dir) not in sys.path:
    sys.path.insert(0, str(examples_dir))

# Add site-packages to path
import site
site_packages = site.getsitepackages()
for path in site_packages:
    if path not in sys.path:
        sys.path.append(path)
