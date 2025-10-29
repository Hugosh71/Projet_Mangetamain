import pandas as pd

from mangetamain.preprocessing.feature.seasonality.analyzers import (
    SeasonalityAnalyzer,
)
from mangetamain.preprocessing.feature.seasonality.strategies import (
    SeasonalityCleaning,
    SeasonalityPreprocessing,
)


def test_seasonality_analyser_stub() -> None:
    recipes = pd.DataFrame([{"id": 1, "name": "A"}])
    interactions = pd.DataFrame(
        [{"recipe_id": 1, "date": "2025-01-01"}, {"recipe_id": 2, "date": "2025-07-01"}]
    )
    analyser = SeasonalityAnalyzer()
    result = analyser.analyze(recipes, interactions)
    assert "inter_doy_sin_smooth" in result.table.columns
    assert "inter_doy_cos_smooth" in result.table.columns
    assert "inter_strength" in result.table.columns


def test_seasonality_strategies_stub() -> None:
    recipes = pd.DataFrame([{"id": 1}])
    interactions = pd.DataFrame([{"recipe_id": 1}])
    cleaner = SeasonalityCleaning()
    pre = SeasonalityPreprocessing()
    r2, i2 = cleaner.clean(recipes, interactions)
    assert r2.equals(recipes) and i2.equals(interactions)
    r3, i3 = pre.preprocess(recipes, interactions)
    assert r3.equals(recipes) and i3.equals(interactions)
