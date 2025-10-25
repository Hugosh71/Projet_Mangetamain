from pathlib import Path
import pandas as pd
import pytest

from mangetamain.preprocessing.streamlit import (
    save_recipes_all_feature_data,
)


def test_save_recipes_all_feature_data_missing_cols(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # Patch getter to return a minimal DF without required columns
    from mangetamain.preprocessing import streamlit as st_mod

    monkeypatch.setattr(
        st_mod,
        "get_recipes_all_feature_data",
        lambda: pd.DataFrame({"id": [1], "name": ["A"]}),
    )

    with pytest.raises(ValueError):
        save_recipes_all_feature_data(tmp_path / "recipes_all_feature_data.csv")


def test_save_recipes_all_feature_data_success(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from mangetamain.preprocessing import streamlit as st_mod

    # Build DF with all required columns
    cols = [
        'id', 'name', 'energy_density', 'protein_ratio', 'fat_ratio',
        'nutrient_balance_index', 'inter_doy_sin_smooth',
        'inter_doy_cos_smooth', 'inter_strength', 'n_interactions',
        'bayes_mean', 'minutes_log', 'score_sweet_savory', 
        'score_spicy_mild', 'score_lowcal_rich', 'score_vegetarian_meat',
        'score_solid_liquid', 'score_raw_processed', 'score_western_exotic',
        'cluster', 'pc_1', 'pc_2', 'tags', 'minutes', 'n_steps',
        'n_ingredients', 'rating_mean'
    ]
    df = pd.DataFrame({c: [0] for c in cols})
    df['id'] = [1]
    df['name'] = ['A']

    monkeypatch.setattr(st_mod, "get_recipes_all_feature_data", lambda: df)

    out = tmp_path / "recipes_all_feature_data.csv"
    save_recipes_all_feature_data(out)
    assert out.exists()


