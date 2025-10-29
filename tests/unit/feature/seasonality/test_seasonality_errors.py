from __future__ import annotations

import pandas as pd
import pytest

from mangetamain.preprocessing.feature.seasonality.analyzers import SeasonalityAnalyzer


def test_seasonality_missing_columns_raises() -> None:
    recipes = pd.DataFrame()
    interactions = pd.DataFrame([{"not_date": "2025-01-01", "not_recipe_id": 1}])
    analyser = SeasonalityAnalyzer()
    with pytest.raises(ValueError):
        analyser.analyze(recipes, interactions)


def test_seasonality_invalid_dates_raises() -> None:
    recipes = pd.DataFrame()
    interactions = pd.DataFrame([{"date": "not-a-date", "recipe_id": 1}])
    analyser = SeasonalityAnalyzer()
    with pytest.raises(ValueError):
        analyser.analyze(recipes, interactions)


