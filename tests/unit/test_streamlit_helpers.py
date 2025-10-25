from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import pytest

from mangetamain.preprocessing import streamlit as st_mod


def test_rgb_to_hex_and_passthrough() -> None:
    assert st_mod.rgb_to_hex("rgb(255, 0, 255)") == "#ff00ff"
    # passthrough when format not matched
    assert st_mod.rgb_to_hex("#112233") == "#112233"


def test_get_col_names_subset_and_values() -> None:
    subset = st_mod.get_col_names(["id", "name"])  # mapping
    assert subset["id"] == "ID"
    values = st_mod.get_col_names(["id", "name"], return_values=True)
    assert "ID" in values


def test_remove_outliers_iqr_filters() -> None:
    df = pd.DataFrame({"x": [1, 2, 3, 100], "y": [1, 1, 1, 1]})
    out = st_mod.remove_outliers_iqr(df, ["x"], k=1)
    assert out["x"].max() < 100


def test_min_max_scale_robust_scaler_shape() -> None:
    df = pd.DataFrame({"a": [1.0, 2.0, 3.0], "b": [10.0, 20.0, 30.0]})
    scaled = st_mod.min_max_scale(df, ["a", "b"])
    assert list(scaled.columns) == ["a", "b"]


def test_add_month_labels_writes_texts() -> None:
    fig, ax = plt.subplots()
    st_mod.add_month_labels(ax)
    # 12 months added
    assert len(ax.texts) == 12
    plt.close(fig)


def test_get_tag_cloud_tfidf_and_counts() -> None:
    df = pd.DataFrame(
        {
            "tags": [
                str(["hello world", "spicy", "time-to-make"]),
                str(["hello world", "mild"]),
            ]
        }
    )
    cloud1 = st_mod.get_tag_cloud(df.copy(), "tags", use_tfidf=True)
    cloud2 = st_mod.get_tag_cloud(df.copy(), "tags", use_tfidf=False)
    assert cloud1 is not None
    assert cloud2 is not None


def test_get_cluster_names_and_summary() -> None:
    mapping = st_mod.get_cluster_names()
    assert 0 in mapping

    df = pd.DataFrame(
        {
            "cluster": [0, 0, 1],
            "n_steps": [1, 3, 2],
            "minutes": [10, 20, 30],
            "n_ingredients": [3, 5, 7],
        }
    )
    summary = st_mod.get_cluster_summary(df, 0)
    assert set(summary.keys()) == {
        "n",
        "minutes_mean",
        "n_steps_mean",
        "n_ingredients",
    }


def test_load_recipes_data_fallback_to_s3(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    dummy = pd.DataFrame({"id": [1]})
    # dummy_path = Path("s3://mangetamain/recipes_merged.csv.gz")

    def fake_read_csv(path: str | Path, *args, **kwargs):
        if isinstance(path, str) and path.startswith("s3://mangetamain/"):
            return dummy
        # simulate local file missing
        raise FileNotFoundError("missing")

    # Patch the module's pandas alias to ensure the decorated function sees it
    monkeypatch.setattr(st_mod.pd, "read_csv", fake_read_csv)

    # ensure the FileNotFoundError path is taken
    missing = tmp_path / "missing.csv"
    if missing.exists():
        missing.unlink()
    # Call underlying function to avoid cache interference
    func = getattr(st_mod.load_recipes_data, "__wrapped__", st_mod.load_recipes_data)
    out = func(missing)
    # assert out[1] is dummy_path
    assert out[0].equals(dummy)


def test_get_recipes_all_feature_data_concat(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    a = pd.DataFrame({"id": [1]})
    b = pd.DataFrame({"id": [2]})
    c = pd.DataFrame({"id": [3]})
    d = pd.DataFrame({"id": [4]})
    e = pd.DataFrame({"id": [5]})

    monkeypatch.setattr(st_mod, "get_recipes_rating_feature_data", lambda: a)
    monkeypatch.setattr(st_mod, "get_recipes_seasonality_feature_data", lambda: b)
    monkeypatch.setattr(st_mod, "get_recipes_ingredients_feature_data", lambda: c)
    monkeypatch.setattr(st_mod, "get_recipes_nutrition_feature_data", lambda: d)
    monkeypatch.setattr(st_mod, "get_recipes_steps_feature_data", lambda: e)

    out = st_mod.get_recipes_all_feature_data()
    assert len(out) == 5
