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


class RemoveZeroRatingCleaning(ICleaningStrategy):
    """Simple cleaning: drop zero ratings and NA ratings."""
    def clean(
        self, recipes: pd.DataFrame, interactions: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        interactions_clean = interactions.copy()
        if "rating" in interactions_clean.columns:
            interactions_clean = interactions_clean[
                interactions_clean["rating"] != 0
            ]
            interactions_clean = interactions_clean.dropna(
                subset=["rating"]
            )  # type: ignore[call-overload]
        return recipes.copy(), interactions_clean


class BasicPreprocessing(IPreprocessingStrategy):
    """Add lightweight derived columns useful for basic analysis."""

    def preprocess(
        self, recipes: pd.DataFrame, interactions: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        interactions_pp = interactions.copy()
        if "rating" in interactions_pp.columns:
            interactions_pp["rating_normalized"] = (
                interactions_pp["rating"].astype(float) / 5.0
            )
        return recipes.copy(), interactions_pp


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
        self._cleaning = cleaning or RemoveZeroRatingCleaning()
        self._preprocessing = preprocessing or BasicPreprocessing()

    def clean(
        self, recipes: pd.DataFrame, interactions: pd.DataFrame
    ) -> ProcessedPair:
        recipes_c, interactions_c = self._cleaning.clean(recipes, interactions)
        return ProcessedPair(recipes=recipes_c, interactions=interactions_c)

    def preprocess(
        self, recipes: pd.DataFrame, interactions: pd.DataFrame
    ) -> ProcessedPair:
        recipes_p, interactions_p = self._preprocessing.preprocess(
            recipes, interactions
        )
        return ProcessedPair(recipes=recipes_p, interactions=interactions_p)
