import pandas as pd

from mangetamain.preprocessing.feature.seasonality.analysers import (
    SeasonalityAnalyser,
)
from mangetamain.preprocessing.feature.seasonality.strategies import (
    SeasonalityCleaning,
    SeasonalityPreprocessing,
)


def test_seasonality_analyser_stub() -> None:
    recipes = pd.DataFrame([{"id": 1, "name": "A"}])
    interactions = pd.DataFrame([{"recipe_id": 1}])
    analyser = SeasonalityAnalyser()
    result = analyser.analyze(recipes, interactions)
    assert "_stub" in result.table.columns


def test_seasonality_strategies_stub() -> None:
    recipes = pd.DataFrame([{"id": 1}])
    interactions = pd.DataFrame([{"recipe_id": 1}])
    cleaner = SeasonalityCleaning()
    pre = SeasonalityPreprocessing()
    r2, i2 = cleaner.clean(recipes, interactions)
    assert r2.equals(recipes) and i2.equals(interactions)
    r3, i3 = pre.preprocess(recipes, interactions)
    assert r3.equals(recipes) and i3.equals(interactions)
