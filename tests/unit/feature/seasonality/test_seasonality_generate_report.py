from pathlib import Path

import pandas as pd

from mangetamain.preprocessing.feature.seasonality.analyzers import (
    SeasonalityAnalyzer,
)


def test_seasonality_generate_report(tmp_path: Path) -> None:
    recipes = pd.DataFrame([{"id": 1, "name": "A"}])
    interactions = pd.DataFrame(
        [{"recipe_id": 1, "date": "2025-01-01"}, {"recipe_id": 2, "date": "2025-07-01"}]
    )
    analyser = SeasonalityAnalyzer()
    result = analyser.analyze(recipes, interactions)
    out = analyser.generate_report(result, tmp_path)
    assert "table_path" in out and "summary_path" in out
