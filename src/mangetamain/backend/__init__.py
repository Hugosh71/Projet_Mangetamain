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
    Analyser,
    AnalysisResult,
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
from .factories import ProcessorFactory
from . import rating as rating

__all__ = [
    # Interfaces / ABCs
    "IDataRepository",
    "IValidator",
    "DataProcessor",
    "Analyser",
    "AnalysisResult",
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
    # Submodules
    "rating",
    # Factories
    "ProcessorFactory",
]
