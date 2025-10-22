"""Backend OOP primitives for Mangetamain.

This package contains abstract interfaces, concrete implementations,
and utilities for data access, preprocessing, and analysis following
SOLID principles and reusable design patterns (Factory, Strategy).
"""

from __future__ import annotations

from .interfaces import (
    IDataRepository,
    IValidator,
    DataProcessor,
    ICleaningStrategy,
    IPreprocessingStrategy,
)
from .exceptions import (
    DataError,
    DataNotFoundError,
    DataLoadError,
    ValidationError,
)
from .repositories import CSVDataRepository, RepositoryPaths
from .processors import BasicDataProcessor
from .analyzers import RecipeAnalyzer
from .factories import ProcessorFactory

__all__ = [
    # Interfaces / ABCs
    "IDataRepository",
    "IValidator",
    "DataProcessor",
    "ICleaningStrategy",
    "IPreprocessingStrategy",
    # Exceptions
    "DataError",
    "DataNotFoundError",
    "DataLoadError",
    "ValidationError",
    # Implementations
    "RepositoryPaths",
    "CSVDataRepository",
    "BasicDataProcessor",
    "RecipeAnalyzer",
    # Factories
    "ProcessorFactory",
]
