"""Concrete data processors and default strategies."""

from __future__ import annotations

import logging
from typing import Tuple

import pandas as pd

from .interfaces import (
    DataProcessor,
    ICleaningStrategy,
    IPreprocessingStrategy,
    ProcessedPair,
)


class NoOpCleaning(ICleaningStrategy):
    """No-op cleaning strategy to keep processors generic by default."""

    def clean(
        self, recipes: pd.DataFrame, interactions: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return recipes.copy(), interactions.copy()


class NoOpPreprocessing(IPreprocessingStrategy):
    """No-op preprocessing strategy."""

    def preprocess(
        self, recipes: pd.DataFrame, interactions: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return recipes.copy(), interactions.copy()


class BasicDataProcessor(DataProcessor):
    """Orchestrates cleaning and preprocessing via Strategy pattern."""

    def __init__(
        self,
        repository,
        *,
        cleaning: ICleaningStrategy | None = None,
        preprocessing: IPreprocessingStrategy | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        super().__init__(repository, logger=logger)
        self._cleaning = cleaning or NoOpCleaning()
        self._preprocessing = preprocessing or NoOpPreprocessing()

    def clean(self, recipes: pd.DataFrame, interactions: pd.DataFrame) -> ProcessedPair:
        recipes_c, interactions_c = self._cleaning.clean(recipes, interactions)
        return ProcessedPair(recipes=recipes_c, interactions=interactions_c)

    def preprocess(
        self, recipes: pd.DataFrame, interactions: pd.DataFrame
    ) -> ProcessedPair:
        recipes_p, interactions_p = self._preprocessing.preprocess(
            recipes, interactions
        )
        return ProcessedPair(recipes=recipes_p, interactions=interactions_p)
