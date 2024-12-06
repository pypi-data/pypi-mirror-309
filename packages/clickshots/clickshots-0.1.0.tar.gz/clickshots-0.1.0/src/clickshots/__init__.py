"""
ClickShots
----------
A robust automated screenshot capture system that monitors user interactions.
"""

from .core import main
from .listeners import ScreenshotListener

__version__ = "0.1.0"
__all__ = ["main", "ScreenshotListener"]