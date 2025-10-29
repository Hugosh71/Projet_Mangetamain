"""Backend OOP primitives for Mangetamain.

This package contains abstract interfaces, concrete implementations,
and utilities for data access, preprocessing, and analysis following
SOLID principles and reusable design patterns (Factory, Strategy).
"""

from __future__ import annotations

from .exceptions import (
    DataError,
    DataLoadError,
    DataNotFoundError,
    ValidationError,
)
from .factories import ProcessorFactory
from .feature import ingredients as ingredients
from .feature import nutrition as nutrition
from .feature import rating as rating
from .feature import seasonality as seasonality
from .feature import steps as steps
from .interfaces import (
    Analyser,
    AnalysisResult,
    DataProcessor,
    ICleaningStrategy,
    IDataRepository,
    IPreprocessingStrategy,
    IValidator,
)
from .processors import BasicDataProcessor
from .repositories import CSVDataRepository, RepositoryPaths

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
    "seasonality",
    "ingredients",
    "nutrition",
    "steps",
    # Factories
    "ProcessorFactory",
]
