"""Seasonality strategies (stubs)."""

from __future__ import annotations

import pandas as pd

from ...interfaces import ICleaningStrategy, IPreprocessingStrategy


class SeasonalityCleaning(ICleaningStrategy):
    def clean(
        self, recipes: pd.DataFrame, interactions: pd.DataFrame
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        return recipes, interactions


class SeasonalityPreprocessing(IPreprocessingStrategy):
    def preprocess(
        self, recipes: pd.DataFrame, interactions: pd.DataFrame
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        return recipes, interactions
