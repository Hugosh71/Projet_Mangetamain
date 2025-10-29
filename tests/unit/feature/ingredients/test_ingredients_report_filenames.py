from __future__ import annotations

from pathlib import Path

import pandas as pd

from mangetamain.preprocessing.feature.ingredients.analysers import (
    IngredientsAnalyser,
)


def test_ingredients_report_filenames_and_stub(tmp_path: Path) -> None:
    recipes = pd.DataFrame([{"id": 1, "name": "A"}])
    interactions = pd.DataFrame([{"recipe_id": 1}])
    analyser = IngredientsAnalyser()
    result = analyser.analyze(recipes, interactions)
    # Should be stubbed
    assert "_stub" in result.table.columns

    out = analyser.generate_report(result, tmp_path)
    assert Path(out["table_path"]).name == "ingredients_table.csv"
    assert Path(out["summary_path"]).name == "ingredients_summary.csv"
    assert Path(out["table_path"]).exists()
    assert Path(out["summary_path"]).exists()
