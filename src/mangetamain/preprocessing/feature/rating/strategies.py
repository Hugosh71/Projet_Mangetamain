"""Strategies specific to rating feature processing.

Implements minimal cleaning and preprocessing hooks for rating interactions.
These can be extended to filter invalid ratings, normalize scales, or enforce
consistency across data sources before analysis.
"""

from __future__ import annotations

import pandas as pd

from ...interfaces import ICleaningStrategy, IPreprocessingStrategy


class RatingCleaning(ICleaningStrategy):
    """Cleaning strategy for rating interactions.

    The current implementation is a no-op placeholder. A production version
    could remove ratings outside expected bounds, discard test interactions,
    or reconcile duplicates.
    """

    def clean(
        self, recipes: pd.DataFrame, interactions: pd.DataFrame
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Return cleaned copies of the inputs.

        Args:
            recipes: Recipes dataframe.
            interactions: Interactions dataframe to be cleaned.

        Returns:
            Tuple of possibly transformed ``(recipes, interactions)``.
        """
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
    """Preprocessing strategy for rating interactions.

    The current implementation forwards inputs unchanged. A non-trivial
    variant may add normalized ratings (e.g., divide by 5) or compute per-user
    z-scores to reduce bias.
    """

    def preprocess(
        self, recipes: pd.DataFrame, interactions: pd.DataFrame
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Return preprocessed copies of the inputs.

        Args:
            recipes: Recipes dataframe.
            interactions: Interactions dataframe to be preprocessed.

        Returns:
            Tuple of possibly transformed ``(recipes, interactions)``.
        """
        # interactions_pp = interactions.copy()
        # if "rating" in interactions_pp.columns:
        #     interactions_pp["rating_normalized"] = (
        #         interactions_pp["rating"].astype(float) / 5.0
        #     )
        recipes_pp = recipes.copy()
        interactions_pp = interactions.copy()
        return recipes_pp, interactions_pp
