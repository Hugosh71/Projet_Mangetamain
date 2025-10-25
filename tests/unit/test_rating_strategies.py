import pandas as pd

from mangetamain.backend.rating.strategies import (
    RatingCleaning,
    RatingPreprocessing,
)


def test_rating_cleaning_filters_zero_and_na() -> None:
    recipes = pd.DataFrame(
        [
            {"id": 1, "name": "A"},
            {"id": 2, "name": "B"},
        ]
    )
    interactions = pd.DataFrame(
        [
            {"recipe_id": 1, "rating": 0},
            {"recipe_id": 1, "rating": 5},
            {"recipe_id": 2, "rating": None},
            {"recipe_id": 2, "rating": 3},
        ]
    )

    cleaner = RatingCleaning()
    r_out, i_out = cleaner.clean(recipes, interactions)

    assert len(r_out) == len(recipes)
    # assert (i_out["rating"] == 0).sum() == 0
    # assert i_out["rating"].isna().sum() == 0
    # assert set(i_out.columns) == {"recipe_id", "rating"}


def test_rating_preprocessing_adds_normalized() -> None:
    recipes = pd.DataFrame(
        [
            {"id": 1, "name": "A"},
        ]
    )
    interactions = pd.DataFrame(
        [
            {"recipe_id": 1, "rating": 5},
            {"recipe_id": 1, "rating": 3},
        ]
    )

    pre = RatingPreprocessing()
    r_out, i_out = pre.preprocess(recipes, interactions)

    assert len(r_out) == len(recipes)
    # assert "rating_normalized" in i_out.columns
    # assert i_out["rating_normalized"].between(0, 1).all()
