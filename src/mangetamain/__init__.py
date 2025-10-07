"""Core package for the Mangetamain application."""

__all__ = [
    "__version__",
    "DataPreprocessor",
    "get_top_recipes_cached",
    "get_vegetarian_stats_cached",
    "LoggingSettings",
]

__version__ = "0.1.0"

from .preprocessing import (
    DataPreprocessor,
    get_top_recipes_cached,
    get_vegetarian_stats_cached,
)
from .settings import LoggingSettings
