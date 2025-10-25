import pandas as pd
from mangetamain.backend.rating.analyzers import RatingAnalyser


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


