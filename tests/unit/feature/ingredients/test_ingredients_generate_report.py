from pathlib import Path
import pandas as pd

from mangetamain.preprocessing.feature.ingredients.analysers import (
    IngredientsAnalyser,
)


def test_ingredients_generate_report(tmp_path: Path) -> None:
    recipes = pd.DataFrame([{"id": 1, "name": "A"}])
    interactions = pd.DataFrame([{"recipe_id": 1}])
    analyser = IngredientsAnalyser()
    result = analyser.analyze(recipes, interactions)
    out = analyser.generate_report(result, tmp_path)
    assert "table_path" in out and "summary_path" in out

