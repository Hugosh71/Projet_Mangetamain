"""Seasonality strategies (stubs).

Defines the cleaning and preprocessing strategies used by the seasonality
feature processing pipeline. Strategies follow simple interfaces that return
possibly transformed copies of the input ``recipes`` and ``interactions``
dataframes while preserving schema invariants.
"""

from __future__ import annotations

import pandas as pd

from ...interfaces import ICleaningStrategy, IPreprocessingStrategy


class SeasonalityCleaning(ICleaningStrategy):
    """No-op cleaning step for seasonality inputs.

    This placeholder keeps the pipeline structure uniform. Implementations may
    drop invalid or out-of-range dates, or filter interactions by source.
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


class SeasonalityPreprocessing(IPreprocessingStrategy):
    """No-op preprocessing step for seasonality inputs.

    Real implementations could compute additional intermediate fields such as
    normalized timestamps or pre-aggregations used by the analyzer.
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
