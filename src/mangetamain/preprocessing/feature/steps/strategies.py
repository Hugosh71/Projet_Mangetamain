"""Steps strategies (stubs).

Defines hooks for cleaning and preprocessing time/steps/ingredients metadata
prior to complexity analysis. Extend these strategies to enforce numeric types
and remove impossible values (e.g., negative minutes).
"""

from __future__ import annotations

import pandas as pd

from ...interfaces import ICleaningStrategy, IPreprocessingStrategy


class StepsCleaning(ICleaningStrategy):
    """No-op cleaning for steps-related fields.

    Useful extensions include clipping outliers or imputing missing values.
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


class StepsPreprocessing(IPreprocessingStrategy):
    """No-op preprocessing for steps-related fields.

    Might compute helper columns used by the analyser.
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
