"""
VirtueRed - CLI tool and Model Server for VirtueAI VirtueRed
"""
# Optionally expose commonly used classes/functions
from .client import ModelServer
from .cli import main

__version__ = "1.2.0"

__all__ = ['ModelServer', 'main']