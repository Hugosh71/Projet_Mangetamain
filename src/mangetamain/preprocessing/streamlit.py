"""Data preprocessing functions for Streamlit application."""

import pandas as pd
import streamlit as st
import numpy as np
import re
from typing import Tuple


@st.cache_data
def load_recipes_data() -> pd.DataFrame:
    """Load and preprocess recipes data from compressed CSV files.

    Returns:
        pd.DataFrame: Combined recipes and clustering data
    """
    # Load recipes data
    recipes_path = "data/preprocessed/recipes_clustering_pca.csv.gz"
    recipes_df = pd.read_csv(recipes_path)

    return recipes_df


def create_visualization_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create additional features for visualization purposes.

    Args:
        df: Input dataframe

    Returns:
        pd.DataFrame: Dataframe with additional features
    """
    # Create mock metrics based on existing data
    np.random.seed(42)  # For reproducibility

    # Metric 1: Rating-like score based on nutrition and steps
    if "nutrition" in df.columns and "n_steps" in df.columns:
        # Extract nutrition values (assuming format like "[51.5, 0.0, 13.0, 0.0, 2.0, 0.0, 4.0]")
        nutrition_scores = []
        for nut in df["nutrition"]:
            try:
                # Parse nutrition string and take first value (calories)
                nut_clean = nut.strip("[]").split(",")[0]
                nutrition_scores.append(float(nut_clean))
            except:
                nutrition_scores.append(0)

        df["metric_1"] = np.array(nutrition_scores) / 100  # Normalize
    else:
        df["metric_1"] = np.random.normal(3, 1, len(df))

    # Metric 2: Time-based metric (minutes)
    if "minutes" in df.columns:
        df["metric_2"] = df["minutes"].fillna(df["minutes"].median())
    else:
        df["metric_2"] = np.random.normal(50, 20, len(df))

    # Ensure positive values
    df["metric_1"] = np.maximum(df["metric_1"], 0.1)
    df["metric_2"] = np.maximum(df["metric_2"], 1)

    # Create ingredients string from ingredients column
    if "ingredients" in df.columns:
        # Convert ingredients list string to comma-separated string
        df["ingredients_clean"] = (
            df["ingredients"].astype(str).str.strip("[]").str.replace("'", "")
        )
    else:
        df["ingredients_clean"] = "unknown"

    # Create tags string from tags column
    if "tags" in df.columns:
        # Convert tags list string to comma-separated string
        df["tags_clean"] = df["tags"].astype(str).str.strip("[]").str.replace("'", "")
    else:
        df["tags_clean"] = "unknown"

    # Rename PCA columns to match expected format
    if "pc_1" in df.columns:
        df["comp_1"] = df["pc_1"]
    if "pc_2" in df.columns:
        df["comp_2"] = df["pc_2"]

    return df


@st.cache_data
def get_cluster_names() -> dict:
    """Get cluster names mapping.

    Returns:
        dict: Mapping of cluster IDs to names
    """
    return {
        0: "Italian Cuisine",
        1: "Asian Cuisine",
        2: "Mediterranean Cuisine",
        3: "Mexican Cuisine",
        4: "French Cuisine",
    }


def get_data_summary(df: pd.DataFrame) -> dict:
    """Get summary statistics for the dataset.

    Args:
        df: Input dataframe

    Returns:
        dict: Summary statistics
    """
    summary = {
        "total_recipes": len(df),
        "total_clusters": df["cluster"].nunique() if "cluster" in df.columns else 0,
        "metric_1_mean": df["metric_1"].mean() if "metric_1" in df.columns else 0,
        "metric_2_mean": df["metric_2"].mean() if "metric_2" in df.columns else 0,
        "clusters": sorted(df["cluster"].unique()) if "cluster" in df.columns else [],
    }
    return summary


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
    match = re.match(r"rgb\((\d+),\s*(\d+),\s*(\d+)\)", rgb_str)
    if match:
        r, g, b = [int(x) for x in match.groups()]
        return "#{:02x}{:02x}{:02x}".format(r, g, b)
    else:
        return rgb_str
