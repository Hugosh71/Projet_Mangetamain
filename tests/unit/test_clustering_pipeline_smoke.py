from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from mangetamain.clustering.pipeline import (
    ClusteringPaths,
    RecipeClusteringPipeline,
)


def _frame(index_values, cols):
    import numpy as np

    df = pd.DataFrame(
        {c: np.random.RandomState(0).rand(len(index_values)) for c in cols},
        index=index_values,
    )
    return df


@pytest.mark.parametrize("n", [25])
def test_pipeline_runs_with_minimal_inputs(tmp_path: Path, n: int) -> None:
    base = tmp_path / "preprocessed"
    out_dir = tmp_path / "clustering"
    base.mkdir(parents=True)
    out_dir.mkdir(parents=True)

    idx = pd.Index(range(n), name="id")
    # nutrition with 4 metrics, plus extra required feature columns will come
    # from others
    nutrition = _frame(
        idx,
        [
            "energy_density",
            "protein_ratio",
            "fat_ratio",
            "nutrient_balance_index",
        ],
    )
    nutrition.to_csv(base / "nutrition_table.csv")

    season = _frame(
        idx,
        [
            "inter_doy_sin_smooth",
            "inter_doy_cos_smooth",
            "inter_strength",
        ],
    )
    season.to_csv(base / "seasonality_table.csv")

    rating = _frame(
        idx,
        [
            "bayes_mean",
            "n_interactions",
            "n_rated",
            "mean_rating",
            "median_rating",
            "rating_std",
        ],
    ).assign(name="r")
    rating.to_csv(base / "rating_table.csv")

    complexity = _frame(
        idx,
        [
            "n_steps_z",
            "n_ingredients_z",
            "minutes_log",
        ],
    )
    complexity.to_csv(base / "complexity_table.csv")

    ingredients = _frame(
        idx,
        [
            "score_sweet_savory",
            "score_spicy_mild",
            "score_lowcal_rich",
            "score_vegetarian_meat",
            "score_solid_liquid",
            "score_raw_processed",
            "score_western_exotic",
        ],
    )
    ingredients.to_csv(base / "ingredients_table.csv")

    paths = ClusteringPaths(base=base, out_dir=out_dir)
    pipe = RecipeClusteringPipeline(paths=paths)
    df = pipe.run()

    assert {"cluster", "pc_1", "pc_2"}.issubset(df.columns)
    out_csv = out_dir / "recipes_clustering_with_pca.csv"
    assert out_csv.exists()
