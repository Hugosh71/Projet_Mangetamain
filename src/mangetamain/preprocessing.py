"""Centralized data preprocessing utilities for the Mangetamain app."""

from dataclasses import dataclass
from typing import Sequence  # noqa: UP035

import pandas as pd
import streamlit as st

from src.mangetamain.utils import read_csv


@dataclass(frozen=True)
class DataPaths:
    """Container for dataset paths used by the preprocessor."""

    recipes_csv: str = "data/RAW_recipes.csv"
    interactions_csv: str = "data/RAW_interactions.csv"


class DataPreprocessor:
    """Provide reusable data loading and transformation for recipes and interactions.

    This class centralizes data preprocessing logic so it can be reused by the
    Streamlit app and other components.
    """

    def __init__(
        self,
        data_paths: DataPaths | None = None,
        recipe_usecols: Sequence[str] | None = ("id", "name"),
        interaction_usecols: Sequence[str] | None = ("recipe_id", "rating"),
    ) -> None:
        self._paths = data_paths or DataPaths()
        self._recipe_usecols = recipe_usecols
        self._interaction_usecols = interaction_usecols

    @property
    def data_paths(self) -> DataPaths:
        """Return the configured data paths (read-only)."""
        return self._paths

    def load_data(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Load recipes and interactions DataFrames.

        Returns a tuple of (df_recipes, df_interactions).
        """
        df_recipes = read_csv(
            self._paths.recipes_csv, usecols=tuple(self._recipe_usecols)
        )
        df_interactions = read_csv(
            self._paths.interactions_csv, usecols=tuple(self._interaction_usecols)
        )
        return df_recipes, df_interactions

    @staticmethod
    def _filter_valid_ratings(df_interactions: pd.DataFrame) -> pd.DataFrame:
        return df_interactions[df_interactions["rating"] != 0]

    @staticmethod
    def _compute_recipe_stats(filtered_interactions: pd.DataFrame) -> pd.DataFrame:
        stats = (
            filtered_interactions.groupby("recipe_id")["rating"]
            .agg(["mean", "std", "count"])
            .fillna({"std": 0})
            .reset_index()
        )
        return stats

    def compute_top_recipes(
        self,
        top_k: int = 10,
        sort_by: Sequence[str] = ("mean", "std", "count"),
        ascending: Sequence[bool] = (False, True, False),
    ) -> pd.DataFrame:
        """Return top-k recipes with statistics merged with recipe names."""
        df_recipes, df_interactions = self.load_data()

        filtered = self._filter_valid_ratings(df_interactions)
        stats = self._compute_recipe_stats(filtered)

        top_stats = (
            stats.sort_values(by=list(sort_by), ascending=list(ascending))
            .head(top_k)
            .reset_index(drop=True)
        )

        top_merged = top_stats.merge(
            df_recipes[["id", "name"]],
            left_on="recipe_id",
            right_on="id",
            how="left",
        )

        formatted = top_merged.rename(
            columns={
                "name": "Nom de la recette",
                "recipe_id": "ID recette",
                "mean": "Note moyenne",
                "std": "Variabilité",
                "count": "Nombre d'évaluations",
            }
        ).assign(
            **{
                "Note moyenne": lambda df: df["Note moyenne"].round(2),
                "Variabilité": lambda df: df["Variabilité"].round(2),
            }
        )[
            [
                "Nom de la recette",
                "ID recette",
                "Note moyenne",
                "Variabilité",
                "Nombre d'évaluations",
            ]
        ]

        return formatted

    def compute_vegetarian_stats(self) -> pd.DataFrame:
        """Compute statistics comparing vegetarian vs meat recipes."""
        meat_tags = ["meat", "chicken", "pork", "turkey", "fish", "beef", "lamb"]
        df_recipes, df_interactions = self.load_data()
        df_interactions["date"] = pd.to_datetime(
            df_interactions["date"], errors="coerce"
        )
        df_interactions["month"] = df_interactions["date"].dt.month

        filtered = self._filter_valid_ratings(df_interactions)
        filtered = pd.merge(
            df_recipes[["id", "tags"]],
            filtered,
            left_on="id",
            right_on="recipe_id",
            how="inner",
        )

        filtered["type"] = "autre"
        filtered.loc[
            filtered["tags"].str.contains("vegetarian|vegan", case=False, na=False),
            "type",
        ] = "végétarien"
        filtered.loc[
            filtered["tags"].str.contains("|".join(meat_tags), case=False, na=False),
            "type",
        ] = "viande"

        monthly_counts = (
            filtered.groupby(["month", "type"]).size().reset_index(name="count")
        )
        monthly_total = monthly_counts.groupby("month")["count"].transform("sum")
        monthly_counts["ratio"] = monthly_counts["count"] / monthly_total
        monthly_pivot = monthly_counts.pivot(
            index="month", columns="type", values="ratio"
        ).fillna(0)

        stats = (
            filtered.groupby("type")
            .agg(
                mean_rating=("rating", "mean"),
                count_rating=("rating", "count"),
                unique_recipes=("recipe_id", "nunique"),
            )
            .reset_index()
            .sort_values(by="mean_rating", ascending=False)
            .reset_index(drop=True)
        )

        results = {
            "monthly_ratios": monthly_pivot.reset_index(),
            "stats": stats,
        }

        print(results["monthly_ratios"])
        print(results["stats"])

        return results


@st.cache_data(persist="disk", show_spinner=False, ttl=None)
def get_top_recipes_cached(
    top_k: int = 10,
    sort_by: tuple[str, ...] = ("mean", "std", "count"),
    ascending: tuple[bool, ...] = (False, True, False),
):
    """Cached accessor to compute top recipes with given parameters."""
    preprocessor = DataPreprocessor(data_paths=DataPaths())
    return preprocessor.compute_top_recipes(
        top_k=top_k, sort_by=list(sort_by), ascending=list(ascending)
    )


@st.cache_data(persist="disk", show_spinner=False, ttl=None)
def get_vegetarian_stats_cached():
    """Cached accessor to compute vegetarian recipe statistics."""
    preprocessor = DataPreprocessor(
        data_paths=DataPaths(),
        recipe_usecols=["id", "name", "tags"],
        interaction_usecols=["recipe_id", "rating", "date"],
    )
    return preprocessor.compute_vegetarian_stats()
