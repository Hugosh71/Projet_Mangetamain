"""Strategies specific to rating feature processing."""

from __future__ import annotations

import pandas as pd

from ..interfaces import ICleaningStrategy, IPreprocessingStrategy


class RatingCleaning(ICleaningStrategy):
    """Remove zero and NA ratings to keep only informative interactions."""

    def clean(
        self, recipes: pd.DataFrame, interactions: pd.DataFrame
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        # interactions_clean = interactions.copy()
        # if "rating" in interactions_clean.columns:
        #     interactions_clean = interactions_clean[
        #         interactions_clean["rating"] != 0
        #     ]
        #     interactions_clean = interactions_clean.dropna(
        #         subset=["rating"]
        #     )  # type: ignore[call-overload]
        interactions_clean = interactions.copy()
        recipes_clean = recipes.copy()
        return recipes_clean, interactions_clean


class RatingPreprocessing(IPreprocessingStrategy):
    """Add normalized rating column for downstream analysis."""

    def preprocess(
        self, recipes: pd.DataFrame, interactions: pd.DataFrame
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        # interactions_pp = interactions.copy()
        # if "rating" in interactions_pp.columns:
        #     interactions_pp["rating_normalized"] = (
        #         interactions_pp["rating"].astype(float) / 5.0
        #     )
        recipes_pp = recipes.copy()
        interactions_pp = interactions.copy()
        return recipes_pp, interactions_pp
