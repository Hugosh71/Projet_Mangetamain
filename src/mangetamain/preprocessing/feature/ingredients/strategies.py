"""Ingredients strategies (stubs).

Hooks for cleaning and preprocessing recipe ingredients. These strategies can
normalize textual ingredients, fix encoding issues, or apply vocabulary
mapping to improve downstream analysis.
"""

from __future__ import annotations

import pandas as pd

from ...interfaces import ICleaningStrategy, IPreprocessingStrategy


class IngredientsCleaning(ICleaningStrategy):
    """No-op cleaning for ingredients.

    May remove empty or malformed ingredient lists and standardize casing.
    """

    def clean(
        self, recipes: pd.DataFrame, interactions: pd.DataFrame
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Return cleaned copies of the inputs.

        Args:
            recipes: Recipes dataframe.
            interactions: Interactions dataframe.

        Returns:
            Tuple of possibly transformed ``(recipes, interactions)``.
        """
        return recipes, interactions


class IngredientsPreprocessing(IPreprocessingStrategy):
    """No-op preprocessing for ingredients.

    Could expand stringified lists to proper arrays or tokenize ingredients.
    """

    def preprocess(
        self, recipes: pd.DataFrame, interactions: pd.DataFrame
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Return preprocessed copies of the inputs.

        Args:
            recipes: Recipes dataframe.
            interactions: Interactions dataframe.

        Returns:
            Tuple of possibly transformed ``(recipes, interactions)``.
        """
        return recipes, interactions
