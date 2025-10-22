"""Custom exceptions for backend operations."""

from __future__ import annotations


class DataError(RuntimeError):
    """Base error for data related failures."""


class DataNotFoundError(DataError):
    """Raised when an expected file or resource cannot be located."""


class DataLoadError(DataError):
    """Raised when loading data fails due to format or IO errors."""


class ValidationError(DataError):
    """Raised when data validation fails."""


