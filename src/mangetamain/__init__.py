"""Core package for the Mangetamain application."""

__all__ = [
    "__version__",
    "LoggingSettings",
    "data_processing",
]

__version__ = "0.1.0"

from . import data_processing as data_processing
from .settings import LoggingSettings
