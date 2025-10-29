"""Nutrition strategies (stubs).

Lightweight strategy placeholders for the nutrition feature pipeline. These
classes implement the minimal cleaning and preprocessing interfaces and can be
extended to handle missing values, standardize units, or normalize schemas.
"""

from __future__ import annotations

import pandas as pd

from ...interfaces import ICleaningStrategy, IPreprocessingStrategy


class NutritionCleaning(ICleaningStrategy):
    """No-op cleaning for nutrition inputs.

    Potential responsibilities include dropping rows with malformed
    ``nutrition`` fields or coercing numeric types.
    """
    def clean(
        self, recipes: pd.DataFrame, interactions: pd.DataFrame
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Return cleaned copies of the inputs.

        Args:
            recipes: Recipes dataframe.
            interactions: Interactions dataframe (unused here).

        Returns:
            Tuple of possibly transformed ``(recipes, interactions)``.
        """
        return recipes, interactions


class NutritionPreprocessing(IPreprocessingStrategy):
    """No-op preprocessing for nutrition inputs.

    Could expand list-like nutrition fields to structured columns or compute
    derived fields required by downstream analysers.
    """
    def preprocess(
        self, recipes: pd.DataFrame, interactions: pd.DataFrame
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Return preprocessed copies of the inputs.

        Args:
            recipes: Recipes dataframe.
            interactions: Interactions dataframe (unused here).

        Returns:
            Tuple of possibly transformed ``(recipes, interactions)``.
        """
        return recipes, interactions
