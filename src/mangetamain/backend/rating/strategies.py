"""Strategies specific to rating feature processing."""

from __future__ import annotations

from typing import Tuple

import pandas as pd

from ..interfaces import ICleaningStrategy, IPreprocessingStrategy


class RatingCleaning(ICleaningStrategy):
    """Remove zero and NA ratings to keep only informative interactions."""

    def clean(
        self, recipes: pd.DataFrame, interactions: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        # interactions_clean = interactions.copy()
        # if "rating" in interactions_clean.columns:
        #     interactions_clean = interactions_clean[
        #         interactions_clean["rating"] != 0
        #     ]
        #     interactions_clean = interactions_clean.dropna(
        #         subset=["rating"]
        #     )  # type: ignore[call-overload]
        return recipes.copy(), interactions.copy()


class RatingPreprocessing(IPreprocessingStrategy):
    """Add normalized rating column for downstream analysis."""

    def preprocess(
        self, recipes: pd.DataFrame, interactions: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        # interactions_pp = interactions.copy()
        # if "rating" in interactions_pp.columns:
        #     interactions_pp["rating_normalized"] = (
        #         interactions_pp["rating"].astype(float) / 5.0
        #     )
        return recipes.copy(), interactions.copy()

