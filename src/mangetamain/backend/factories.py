"""Factories to assemble backend components with sensible defaults."""
from __future__ import annotations

import logging
from .processors import (
    BasicDataProcessor,
    BasicPreprocessing,
    RemoveZeroRatingCleaning,
)


class ProcessorFactory:
    """Build preconfigured processors with default strategies."""

    @staticmethod
    def create_basic(
        repository, *, logger: logging.Logger | None = None
    ) -> BasicDataProcessor:
        return BasicDataProcessor(
            repository,
            cleaning=RemoveZeroRatingCleaning(),
            preprocessing=BasicPreprocessing(),
            logger=logger,
        )
