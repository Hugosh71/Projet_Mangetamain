"""Core package for the Mangetamain application."""

__all__ = [
    "__version__",
    "LoggingSettings",
    "backend",
]

__version__ = "0.1.0"

from .settings import LoggingSettings
from . import backend as backend
