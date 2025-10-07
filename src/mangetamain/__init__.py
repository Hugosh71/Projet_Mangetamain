"""Core package for the Mangetamain application."""

__all__ = [
    "__version__",
    "DataPreprocessor",
    "get_top_recipes_cached",
]

__version__ = "0.1.0"

from .preprocessing import DataPreprocessor, get_top_recipes_cached  # re-export for convenience
