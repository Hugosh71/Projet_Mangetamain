import pandas as pd
import pytest
from mangetamain.preprocessing.feature.rating.analyzers import RatingAnalyser


# def test_no_interactions() -> None:
#     recipes = pd.DataFrame([
#         {"id": 1, "name": "A"},
#     ])
#     interactions = pd.DataFrame([], columns=["recipe_id", "rating"])  # empty

#     analyser = RatingAnalyser()
#     result = analyser.analyze(recipes, interactions)
#     table = result.table

#     # Should have n_interactions = 0, n_rated = 0
#     assert (table["n_interactions"] == 0).all()
#     assert (table["n_rated"] == 0).all()


def test_all_zero_ratings() -> None:
    recipes = pd.DataFrame([
        {"id": 1, "name": "A"},
    ])
    interactions = pd.DataFrame([
        {"recipe_id": 1, "rating": 0},
        {"recipe_id": 1, "rating": 0},
    ])

    analyser = RatingAnalyser()
    result = analyser.analyze(recipes, interactions)
    table = result.table

    # No rated entries
    assert (table["n_rated"] == 0).all()
    # mean/median can be NaN; share_rated should be 0
    assert (table["share_rated"] == 0).all()

def test_with_wilson_per_recipe() -> None:
    recipes = pd.DataFrame([
        {"id": 1, "name": "A"},
        {"id": 2, "name": "B"},
        {"id": 3, "name": "C"},
    ])
    interactions = pd.DataFrame([
        {"recipe_id": 1, "rating": 0},
        {"recipe_id": 1, "rating": 5},
        {"recipe_id": 2, "rating": 4},
        {"recipe_id": 3, "rating": 1},
        {"recipe_id": 3, "rating": 1},
        {"recipe_id": 3, "rating": 1},
    ])
    analyser = RatingAnalyser()
    result = analyser.analyze(recipes, interactions, with_wilson_per_recipe=True)
    table = result.table
    assert (table["wilson_low_rec"] <= table["share_rated"]).all()
    assert (table["wilson_high_rec"] >= table["share_rated"]).all()

def test_recipe_id_not_in_interactions() -> None:
    recipes = pd.DataFrame([
        {"id": 1, "name": "A"},
    ])
    interactions = pd.DataFrame([
        {"user_id": 1, "rating": 0},
    ])
    with pytest.raises(ValueError) as e:
        analyser = RatingAnalyser()
        analyser.analyze(recipes, interactions)
    assert "interactions must contain 'recipe_id'" in str(e)