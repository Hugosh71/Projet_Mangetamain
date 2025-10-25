from __future__ import annotations
from pathlib import Path
import pandas as pd

from mangetamain.preprocessing.feature.rating.analyzers import RatingAnalyser


def test_analyze_handles_zero_ratings() -> None:
    recipes = pd.DataFrame([
        {"id": 1, "name": "A"},
    ])
    # interactions with zero ratings (no rated entries)
    interactions = pd.DataFrame([
        {"recipe_id": 1, "rating": 0},
        {"recipe_id": 1, "rating": 0},
    ])

    analyser = RatingAnalyser()
    result = analyser.analyze(recipes, interactions)

    # Ensure table was computed and contains expected basic columns
    table = result.table
    assert {"recipe_id", "n_interactions", "n_rated"}.issubset(table.columns)


def test_generate_report_with_file_path_outputs_to_parent(
    tmp_path: Path,
) -> None:
    recipes = pd.DataFrame([
        {"id": 1, "name": "A"},
    ])
    interactions = pd.DataFrame([
        {"recipe_id": 1, "rating": 5},
    ])

    analyser = RatingAnalyser()
    result = analyser.analyze(recipes, interactions)

    out_file = tmp_path / "dummy.txt"
    report = analyser.generate_report(result, out_file)

    # Files should be placed in parent directory of the file
    assert (tmp_path / "rating_table.csv").exists()
    assert (tmp_path / "rating_summary.csv").exists()
    assert Path(report["table_path"]).exists()
    assert Path(report["summary_path"]).exists()
