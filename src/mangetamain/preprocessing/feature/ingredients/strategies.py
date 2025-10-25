"""Ingredients strategies (stubs)."""

from __future__ import annotations

from typing import Tuple
import pandas as pd

from ...interfaces import ICleaningStrategy, IPreprocessingStrategy


class IngredientsCleaning(ICleaningStrategy):
    def clean(
        self, recipes: pd.DataFrame, interactions: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return recipes, interactions


class IngredientsPreprocessing(IPreprocessingStrategy):
    def preprocess(
        self, recipes: pd.DataFrame, interactions: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return recipes, interactions


