"""Core package for the Mangetamain application."""

__all__ = [
    "__version__",
    "LoggingSettings",
    "backend",
]

__version__ = "0.1.0"

from . import backend as backend
from .settings import LoggingSettings
