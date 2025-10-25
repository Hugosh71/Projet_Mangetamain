"""Nutrition strategies (stubs)."""

from __future__ import annotations

from typing import Tuple
import pandas as pd

from ..interfaces import ICleaningStrategy, IPreprocessingStrategy


class NutritionCleaning(ICleaningStrategy):
    def clean(
        self, recipes: pd.DataFrame, interactions: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return recipes, interactions


class NutritionPreprocessing(IPreprocessingStrategy):
    def preprocess(
        self, recipes: pd.DataFrame, interactions: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return recipes, interactions


