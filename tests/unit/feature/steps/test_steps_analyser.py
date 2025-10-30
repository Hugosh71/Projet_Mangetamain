import pandas as pd

from mangetamain.preprocessing.feature.steps.analysers import (
    StepsAnalyser,
)
from mangetamain.preprocessing.feature.steps.strategies import (
    StepsCleaning,
    StepsPreprocessing,
)


def test_steps_analyser() -> None:
    recipes = pd.DataFrame(
        {
            "minutes": [10, 20, 30, 40, 50],
            "n_steps": [3, 5, 7, 2, 6],
            "n_ingredients": [4, 6, 8, 3, 7],
            "id": [1, 2, 3, 4, 5],
        }
    )
    interactions = pd.DataFrame(
        [
            [
                {"recipe_id": 1, "date": "2025-01-01"},
                {"recipe_id": 2, "date": "2025-07-01"},
            ]
        ]
    )
    analyser = StepsAnalyser()
    result = analyser.analyze(recipes, interactions)
    assert "id" in result.table.columns
    assert "minutes" in result.table.columns
    assert "n_steps" in result.table.columns
    assert "n_ingredients" in result.table.columns


def test_steps_strategies() -> None:
    recipes = pd.DataFrame(
        {
            "minutes": [10, 20, 30, 40, 50],
            "n_steps": [3, 5, 7, 2, 6],
            "n_ingredients": [4, 6, 8, 3, 7],
            "id": [1, 2, 3, 4, 5],
        }
    )
    interactions = pd.DataFrame(
        [
            [
                {"recipe_id": 1, "date": "2025-01-01"},
                {"recipe_id": 2, "date": "2025-07-01"},
            ]
        ]
    )
    cleaner = StepsCleaning()
    pre = StepsPreprocessing()
    r2, i2 = cleaner.clean(recipes, interactions)
    assert r2.equals(recipes) and i2.equals(interactions)
    r3, i3 = pre.preprocess(recipes, interactions)
    assert r3.equals(recipes) and i3.equals(interactions)
