from __future__ import annotations

from pathlib import Path

import pandas as pd

from mangetamain.preprocessing.feature.nutrition.analysers import NutritionAnalyser


def test_nutrition_analyse_and_report_real_path(tmp_path: Path) -> None:
    # nutrition is a list of 7 numbers: [calories, fat, sugar, sodium, protein, sat_fat, carbs]
    recipes = pd.DataFrame(
        [
            {"id": 1, "name": "A", "nutrition": "[100, 10, 5, 200, 20, 3, 30]"},
            {"id": 2, "name": "B", "nutrition": "[200, 20, 10, 400, 30, 4, 50]"},
        ]
    )
    interactions = pd.DataFrame()

    analyser = NutritionAnalyser()
    result = analyser.analyze(recipes, interactions)

    # Expected feature columns should exist
    for col in [
        "energy_density",
        "protein_ratio",
        "fat_ratio",
        "nutrient_balance_index",
    ]:
        assert col in result.table.columns

    out = analyser.generate_report(result, tmp_path)
    assert Path(out["table_path"]).name == "nutrition_table.csv"
    assert Path(out["summary_path"]).name == "nutrition_summary.csv"
    assert Path(out["table_path"]).exists()
    assert Path(out["summary_path"]).exists()
