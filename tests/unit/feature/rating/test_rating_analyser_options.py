import pandas as pd

from mangetamain.preprocessing.feature.rating.analyzers import RatingAnalyser


def test_rating_analyser_with_params_and_wilson() -> None:
    recipes = pd.DataFrame(
        [
            {"id": 1, "name": "A"},
            {"id": 2, "name": "B"},
        ]
    )
    interactions = pd.DataFrame(
        [
            {"recipe_id": 1, "rating": 5},
            {"recipe_id": 2, "rating": 0},
            {"recipe_id": 2, "rating": 4},
        ]
    )

    analyser = RatingAnalyser()
    result = analyser.analyze(
        recipes,
        interactions,
        c=10,
        mu_percentile=0.75,
        with_wilson_per_recipe=True,
    )
    table = result.table

    # Wilson columns should exist when option enabled
    assert {"wilson_low_rec", "wilson_high_rec"}.issubset(set(table.columns))
    # bayes_mean should be finite
    assert table["bayes_mean"].notna().all()
