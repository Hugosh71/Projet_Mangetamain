from pathlib import Path

import pandas as pd

from mangetamain.preprocessing.feature.steps.analysers import (
    StepsAnalyser,
)


def test_steps_generate_report(tmp_path: Path) -> None:
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
    out = analyser.generate_report(result, tmp_path)
    assert "table_path" in out and "summary_path" in out
