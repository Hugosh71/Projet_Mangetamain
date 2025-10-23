"""Data preprocessing functions for Streamlit application."""

import re

import numpy as np
import pandas as pd
import streamlit as st


@st.cache_data
def load_recipes_data() -> pd.DataFrame:
    """Load and preprocess recipes data from compressed CSV files.

    Returns:
        pd.DataFrame: Combined recipes and clustering data
    """
    # Load recipes data
    recipes_path = "data/preprocessed/recipes_merged.csv.gz"
    recipes_df = pd.read_csv(recipes_path)
    print(recipes_df)

    return recipes_df


@st.cache_data
def get_cluster_names() -> dict:
    """Get cluster names mapping.

    Returns:
        dict: Mapping of cluster IDs to names
    """
    return {
        0: "Plats complets équilibrés et élaborés",
        1: "Plats simples et salés",
        2: "Recettes sucrées et riches",
        3: "Snacks sucrés ultra riches",
        4: "Repas rapides semi-équilibrés",
    }


@st.cache_data
def get_col_names(cols=None, return_values=False) -> dict:
    """Get column names mapping.
    Args:
        cols (list, optional): List of column keys to get names for.
        If None, return all.
    Returns:
        dict: Mapping of column keys to French names
    """

    col_map = {
        "id": "ID",
        "name": "Nom de recette",
        "energy_density": "Densité énergétique",
        "protein_ratio": "Proportion de protéines par calorie",
        "fat_ratio": "Proportion de lipides par calorie",
        "nutrient_balance_index": "Indice d'équilibre nutritionnel",
        "score_sweet_savory": "Sucré → Salé",
        "score_spicy_mild": "Épicé → Doux",
        "score_lowcal_rich": "Léger → Riche",
        "score_vegetarian_meat": "Végétarien → Carné",
        "score_solid_liquid": "Solide → Liquide",
        "score_raw_processed": "Cru → Transformé",
        "score_western_exotic": "Occidental → Exotique",
        "rating_mean": "Note moyenne",
    }

    if cols is not None:
        col_names = {col: col_map[col] for col in cols if col in col_map}
    else:
        col_names = col_map

    if return_values:
        return list(col_names.values())
    else:
        return col_names


def remove_outliers_iqr(df, cols, k=5):
    """Remove outliers from specified columns using the IQR method."""
    df_filtered = df.copy()
    for col in cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - k * iqr
        upper = q3 + k * iqr
        df_filtered = df_filtered[
            (df_filtered[col] >= lower) & (df_filtered[col] <= upper)
        ]
    return df_filtered


def add_month_labels(ax):
    """Add French month labels (Jan–Déc) around the unit circle."""
    month_mid_doy = [15, 46, 74, 105, 135, 166, 196, 227, 258, 288, 319, 349]
    month_labels_fr = [
        "Jan",
        "Fév",
        "Mar",
        "Avr",
        "Mai",
        "Jui",
        "Juil",
        "Aoû",
        "Sep",
        "Oct",
        "Nov",
        "Déc",
    ]

    for month, doy in enumerate(month_mid_doy):
        theta = 2 * np.pi * doy / 365
        x = np.cos(theta) * 1.08
        y = np.sin(theta) * 1.08
        ax.text(
            x,
            y,
            month_labels_fr[month],
            ha="center",
            va="center",
            fontsize=9,
            fontweight="bold",
        )


def rgb_to_hex(rgb_str):
    """Convert RGB string to HEX format.
    Args:
        rgb_str: RGB string in the format "rgb(r, g, b)"
    Returns:
        str: HEX color string
    """

    match = re.match(r"rgb\((\d+),\s*(\d+),\s*(\d+)\)", rgb_str)
    if match:
        r, g, b = [int(x) for x in match.groups()]
        return f"#{r:02x}{g:02x}{b:02x}"
    else:
        return rgb_str


def min_max_scale(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    """Apply Min-Max scaling to specified columns in the dataframe.

    Args:
        df: Input dataframe
        columns: List of column names to scale

    Returns:
        pd.DataFrame: DataFrame with scaled columns
    """
    df_scaled = df.copy()
    for col in cols:
        min_val = df[col].min()
        max_val = df[col].max()
        df_scaled[col] = (df[col] - min_val) / (max_val - min_val)
    return df_scaled
