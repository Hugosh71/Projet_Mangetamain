"""Unit tests for RecipeSeasonalityFeatureBuilder."""

import numpy as np
import pandas as pd
import pytest

from mangetamain.preprocessing.feature_engineering import (
    RecipeSeasonalityFeatureBuilder,
)


@pytest.fixture
def interactions_df():
    # Interactions across three recipes with different seasonal patterns
    return pd.DataFrame(
        {
            "recipe_id": [1, 1, 1, 2, 2, 3, 3, 3],
            "date": [
                "2023-01-01",
                "2023-01-15",
                "2023-02-01",
                "2023-06-15",
                "2023-07-01",
                "2023-12-01",
                "2023-12-15",
                "2023-12-31",
            ],
            "rating": [4, 5, 3, 4, 5, 2, 3, 4],
        }
    )


@pytest.fixture
def recipes_df():
    # Recipes table, includes one unseen recipe (id=4)
    return pd.DataFrame({"id": [1, 2, 3, 4], "title": ["A", "B", "C", "D"]})


def test_fit_basic(interactions_df):
    builder = RecipeSeasonalityFeatureBuilder()
    result = builder.fit(interactions_df)

    # fit returns self
    assert result is builder

    # globals computed
    assert builder.sin_global_ is not None
    assert builder.cos_global_ is not None
    assert isinstance(builder.sin_global_, float)
    assert isinstance(builder.cos_global_, float)

    # feature_df_ exists with expected columns
    assert builder.feature_df_ is not None
    expected_cols = {
        "recipe_id",
        "inter_doy_sin_smooth",
        "inter_doy_cos_smooth",
        "inter_strength",
    }
    assert expected_cols.issubset(set(builder.feature_df_.columns))


def test_fit_validates_required_columns():
    builder = RecipeSeasonalityFeatureBuilder()
    with pytest.raises(ValueError, match="must contain 'date' and 'recipe_id'"):
        builder.fit(pd.DataFrame({"x": [1]}))


def test_fit_invalid_dates_raises():
    builder = RecipeSeasonalityFeatureBuilder()
    bad = pd.DataFrame({"recipe_id": [1], "date": ["not-a-date"]})
    with pytest.raises(ValueError, match="Invalid dates found"):
        builder.fit(bad)


def test_transform_requires_fit(recipes_df):
    builder = RecipeSeasonalityFeatureBuilder()
    with pytest.raises(RuntimeError, match="Must fit on interactions"):
        builder.transform(recipes_df)


def test_transform_merge_and_fillna(interactions_df, recipes_df):
    builder = RecipeSeasonalityFeatureBuilder()
    builder.fit(interactions_df)

    out = builder.transform(recipes_df)

    # preserves original columns and adds seasonal features
    for col in [
        "id",
        "title",
        "inter_doy_sin_smooth",
        "inter_doy_cos_smooth",
        "inter_strength",
    ]:
        assert col in out.columns

    # rows preserved
    assert len(out) == len(recipes_df)

    # unseen recipe id=4 filled with globals / 0 strength
    unseen = out[out["id"] == 4].iloc[0]
    assert np.isclose(unseen["inter_doy_sin_smooth"], builder.sin_global_)
    assert np.isclose(unseen["inter_doy_cos_smooth"], builder.cos_global_)
    assert np.isclose(unseen["inter_strength"], 0.0)


def test_inputs_not_mutated(interactions_df, recipes_df):
    builder = RecipeSeasonalityFeatureBuilder()
    interactions_copy = interactions_df.copy()
    recipes_copy = recipes_df.copy()

    builder.fit(interactions_df)
    builder.transform(recipes_df)

    pd.testing.assert_frame_equal(interactions_df, interactions_copy)
    pd.testing.assert_frame_equal(recipes_df, recipes_copy)


def test_custom_column_names():
    df = pd.DataFrame(
        {
            "item": [10, 10, 11],
            "when": ["2023-01-01", "2023-06-01", "2023-12-01"],
        }
    )
    items = pd.DataFrame({"id": [10, 11, 12]})

    builder = RecipeSeasonalityFeatureBuilder(date_col="when", group_col="item", k=3.0)
    builder.fit(df)
    out = builder.transform(items)

    assert {"inter_doy_sin_smooth", "inter_doy_cos_smooth", "inter_strength"}.issubset(
        set(out.columns)
    )
    assert len(out) == 3
