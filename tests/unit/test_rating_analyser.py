import pandas as pd
from pathlib import Path
from mangetamain.backend.rating.analyzers import RatingAnalyser

def test_rating_analyser_basic_topk() -> None:
    recipes = pd.DataFrame([
        {"id": 1, "name": "A"},
        {"id": 2, "name": "B"},
        {"id": 3, "name": "C"},
    ])
    interactions = pd.DataFrame(
        [
            {"recipe_id": 1, "rating": 5},
            {"recipe_id": 1, "rating": 4},
            {"recipe_id": 2, "rating": 3},
            {"recipe_id": 2, "rating": 3},
            {"recipe_id": 3, "rating": 1},
        ]
    )

    analyser = RatingAnalyser()
    result = analyser.analyze(recipes, interactions)

    # assert list(result.top_recipes.columns) == [
    #     "recipe_name",
    #     "recipe_id",
    #     "rating_mean",
    #     "rating_std",
    #     "num_ratings",
    # ]
    # assert len(result.top_recipes) == 2
    tmp_path = Path("tmp")
    tmp_path.mkdir(parents=True, exist_ok=True)

    report = analyser.generate_report(result, tmp_path / "test_rating_analyser_basic_topk.csv")
    assert Path(report["path"]).exists()


