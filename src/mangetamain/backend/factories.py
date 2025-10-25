"""Factories to assemble backend components with sensible defaults."""

from __future__ import annotations

import logging
from .processors import (
    BasicDataProcessor,
    NoOpPreprocessing,
    NoOpCleaning,
)
from .rating import RatingCleaning, RatingPreprocessing


class ProcessorFactory:
    """Build preconfigured processors with default strategies."""

    @staticmethod
    def create_basic(
        repository, *, logger: logging.Logger | None = None
    ) -> BasicDataProcessor:
        return BasicDataProcessor(
            repository,
            cleaning=NoOpCleaning(),
            preprocessing=NoOpPreprocessing(),
            logger=logger,
        )

    @staticmethod
    def create_rating(
        repository, *, logger: logging.Logger | None = None
    ) -> BasicDataProcessor:
        return BasicDataProcessor(
            repository,
            cleaning=RatingCleaning(),
            preprocessing=RatingPreprocessing(),
            logger=logger,
        )
