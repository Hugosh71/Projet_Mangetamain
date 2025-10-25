"""Steps strategies (stubs)."""

from __future__ import annotations

from typing import Tuple
import pandas as pd

from ..interfaces import ICleaningStrategy, IPreprocessingStrategy


class StepsCleaning(ICleaningStrategy):
    def clean(
        self, recipes: pd.DataFrame, interactions: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return recipes, interactions


class StepsPreprocessing(IPreprocessingStrategy):
    def preprocess(
        self, recipes: pd.DataFrame, interactions: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return recipes, interactions


