from pathlib import Path

import pandas as pd
import pytest

from mangetamain.preprocessing import (
    DataPaths,
    DataPreprocessor,
    get_top_recipes_cached,
    get_vegetarian_stats_cached,
)


@pytest.fixture()
def tmp_csvs(tmp_path: Path) -> tuple[DataPaths, pd.DataFrame, pd.DataFrame]:
    recipes = pd.DataFrame(
        [
            {"id": 1, "name": "Salade", "tags": "vegetarian, quick"},
            {"id": 2, "name": "Poulet rôti", "tags": "chicken, dinner"},
            {"id": 3, "name": "Boeuf", "tags": "beef"},
            {"id": 4, "name": "Tofu sauté", "tags": "vegetarian"},
        ]
    )
    interactions = pd.DataFrame(
        [
            {"recipe_id": 1, "rating": 5},
            {"recipe_id": 1, "rating": 4},
            {"recipe_id": 2, "rating": 0},  # should be filtered out
            {"recipe_id": 2, "rating": 3},
            {"recipe_id": 3, "rating": 2},
            {"recipe_id": 3, "rating": 3},
            {"recipe_id": 4, "rating": 5},
        ]
    )

    recipes_path = tmp_path / "recipes.csv"
    interactions_path = tmp_path / "interactions.csv"
    recipes.to_csv(recipes_path, index=False)
    interactions.to_csv(interactions_path, index=False)

    paths = DataPaths(
        recipes_csv=str(recipes_path), interactions_csv=str(interactions_path)
    )
    return paths, recipes, interactions


def test_load_data(tmp_csvs: tuple[DataPaths, pd.DataFrame, pd.DataFrame]) -> None:
    paths, recipes_df, interactions_df = tmp_csvs
    pre = DataPreprocessor(
        data_paths=paths,
        recipe_usecols=["id", "name", "tags"],
        interaction_usecols=["recipe_id", "rating"],
    )
    loaded_recipes, loaded_interactions = pre.load_data()

    assert set(loaded_recipes.columns) >= {"id", "name"}
    assert set(loaded_interactions.columns) == {"recipe_id", "rating"}
    assert len(loaded_recipes) == len(recipes_df)
    assert len(loaded_interactions) == len(interactions_df)


def test_compute_top_recipes_basic(
    tmp_csvs: tuple[DataPaths, pd.DataFrame, pd.DataFrame],
) -> None:
    paths, _, _ = tmp_csvs
    pre = DataPreprocessor(data_paths=paths)

    top = pre.compute_top_recipes(top_k=3)

    # Expected columns and rounding
    assert list(top.columns) == [
        "Nom de la recette",
        "ID recette",
        "Note moyenne",
        "Variabilité",
        "Nombre d'évaluations",
    ]

    assert top["Note moyenne"].dtype.kind in {"i", "f"}
    assert (top["ID recette"] == 2).any()

    # Sorting: highest mean first, then lowest std
    means = top["Note moyenne"].tolist()
    assert means == sorted(means, reverse=True)


def test_compute_vegetarian_stats(
    tmp_csvs: tuple[DataPaths, pd.DataFrame, pd.DataFrame],
) -> None:
    paths, _, _ = tmp_csvs
    pre = DataPreprocessor(
        data_paths=paths,
        recipe_usecols=["id", "name", "tags"],
        interaction_usecols=["recipe_id", "rating"],
    )

    stats = pre.compute_vegetarian_stats()

    assert set(stats.columns) == {
        "Type",
        "Note moyenne",
        "Nombre d'évaluations",
        "Nombre de recettes uniques",
    }

    # We expect categories: végétarien, viande, autre (depending on tags)
    assert {"végétarien", "viande"}.issubset(set(stats["Type"]))


def test_cached_accessors(
    tmp_csvs: tuple[DataPaths, pd.DataFrame, pd.DataFrame],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    paths, _, _ = tmp_csvs

    # Bypass Streamlit cache by returning the same function (no-op decorator)
    import mangetamain.preprocessing as prep

    def no_cache_decorator(*_args, **_kwargs):
        def wrap(func):
            return func

        return wrap

    monkeypatch.setattr(prep.st, "cache_data", no_cache_decorator)

    # Point DataPaths used inside cached functions to our temp files
    monkeypatch.setattr(prep, "DataPaths", lambda: paths)

    top = get_top_recipes_cached(top_k=2)
    assert len(top) == 2

    veg_stats = get_vegetarian_stats_cached()
    assert not veg_stats.empty
