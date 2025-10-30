"""Clustering pipeline (PCA + KMeans) for recipe feature tables.

This module loads precomputed feature tables produced by the preprocessing
analysers (nutrition, seasonality, rating, steps/complexity, ingredients),
validates the presence of required columns, and runs a dimensionality
reduction and clustering workflow that mirrors the team notebooks:

- merges inputs on recipe index,
- standardizes selected variables,
- computes PCA with as many components as features,
- applies KMeans to the first N principal components,
- exports a compact CSV with ``cluster``, ``pc_1`` and ``pc_2`` per recipe.

See :class:`RecipeClusteringPipeline` for the public API.
"""

from __future__ import annotations

import logging
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Variables to use, strictly matching the notebook selection order
REQUIRED_FEATURES: list[str] = [
    "energy_density",
    "protein_ratio",
    "fat_ratio",
    "nutrient_balance_index",
    "inter_doy_sin_smooth",
    "inter_doy_cos_smooth",
    "inter_strength",
    "n_interactions",
    "bayes_mean",
    "n_steps_z",
    "n_ingredients_z",
    "minutes_log",
    "score_sweet_savory",
    "score_spicy_mild",
    "score_lowcal_rich",
    "score_vegetarian_meat",
    "score_solid_liquid",
    "score_raw_processed",
    "score_western_exotic",
]


@dataclass(frozen=True)
class ClusteringPaths:
    """Input and output paths for clustering pipeline."""

    base: Path = Path("data/preprocessed")
    out_dir: Path = Path("data/clustering")

    nutrition: str = "nutrition_table.csv"
    seasonality: str = "seasonality_table.csv"
    rating: str = "rating_table.csv"
    complexity: str = "complexity_table.csv"
    ingredients: str = "ingredients_table.csv"

    def input_paths(self) -> dict[str, Path]:
        if not self.base.exists():
            raise FileNotFoundError(f"Base directory not found: {self.base}")

        if not (self.base / self.nutrition).exists():
            self.nutrition = "backup/features_nutrition.csv"
        if not (self.base / self.seasonality).exists():
            self.seasonality = "backup/recipe_seasonality_features.csv"
        if not (self.base / self.rating).exists():
            self.rating = "backup/recipes_feature_rating_full.csv"
        if not (self.base / self.complexity).exists():
            self.complexity = "backup/recipes_features_complexity.csv"
        if not (self.base / self.ingredients).exists():
            self.ingredients = "backup/features_axes_ingredients.csv"
        return {
            "nutrition": self.base / self.nutrition,
            "seasonality": self.base / self.seasonality,
            "rating": self.base / self.rating,
            "complexity": self.base / self.complexity,
            "ingredients": self.base / self.ingredients,
        }

    def output_csv(self) -> Path:
        return self.out_dir / "recipes_clustering_with_pca.csv"


class RecipeClusteringPipeline:
    """Compute PCA and KMeans clustering from preprocessed feature CSVs.

    This reproduces the notebook logic:
      - merge inputs on index
      - StandardScaler on REQUIRED_FEATURES
      - PCA with n_components = len(REQUIRED_FEATURES)
      - KMeans(n_clusters=5, random_state=42) on first 12 PCs
      - Output dataframe with per-recipe cluster, pc_1, pc_2
    """

    def __init__(
        self,
        *,
        paths: ClusteringPaths | None = None,
        logger: logging.Logger | None = None,
        n_clusters: int = 5,
        random_state: int = 42,
        n_pcs_for_kmeans: int = 12,
    ) -> None:
        self.paths = paths or ClusteringPaths()
        self.logger = logger or logging.getLogger("mangetamain.clustering")
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.n_pcs_for_kmeans = n_pcs_for_kmeans

    # ---- public API -----------------------------------------------------
    def run(self) -> pd.DataFrame:
        """Execute the full clustering pipeline and save the CSV output.

        Returns:
            pd.DataFrame: DataFrame indexed by recipe id with columns:
                - name (if available)
                - cluster (int)
                - pc_1 (float)
                - pc_2 (float)
        """
        df = self._load_merge_inputs()
        self._validate_features(df, REQUIRED_FEATURES)

        pca_df, pca_model = self._compute_pca(df[REQUIRED_FEATURES])
        pcs_subset = pca_df.iloc[:, : self.n_pcs_for_kmeans]
        clusters = self._fit_predict_kmeans(pcs_subset)

        result = self._build_result(df, pca_df, clusters)
        self._save_output(result)
        return result

    # ---- steps ----------------------------------------------------------
    def _load_merge_inputs(self) -> pd.DataFrame:
        paths = self.paths.input_paths()
        for key, p in paths.items():
            if not p.exists():
                raise FileNotFoundError(f"Missing input file for {key}: {p}")

        # Respect notebook logic: read as CSV, merge by index
        nutrition = pd.read_csv(
            paths["nutrition"],
            delimiter=(
                ";"
                if paths["nutrition"]
                == Path("data/preprocessed/backup/features_nutrition.csv")
                else None
            ),
            index_col=0,
        )
        seasonal = pd.read_csv(paths["seasonality"], index_col=0)
        rating = pd.read_csv(paths["rating"], index_col=0)
        complexity = pd.read_csv(paths["complexity"], index_col=0)
        ingredients = pd.read_csv(paths["ingredients"], index_col=0)

        recipes = (
            nutrition.merge(seasonal, left_index=True, right_index=True)
            .merge(rating, left_index=True, right_index=True)
            .merge(complexity, left_index=True, right_index=True)
            .merge(ingredients, left_index=True, right_index=True)
        )

        # Normalize name column to a single canonical column if present
        if "name" in recipes.columns:
            recipes.rename(columns={"name": "name"}, inplace=True)
        elif "name_x" in recipes.columns:
            recipes.rename(columns={"name_x": "name"}, inplace=True)

        self.logger.debug(
            "Merged input shapes: %s",
            {
                "nutrition": nutrition.shape,
                "seasonal": seasonal.shape,
                "rating": rating.shape,
                "complexity": complexity.shape,
                "ingredients": ingredients.shape,
            },
        )
        self.logger.info("Merged recipes shape: %s", recipes.shape)
        return recipes

    def _validate_features(self, df: pd.DataFrame, required: Iterable[str]) -> None:
        missing = [c for c in required if c not in df.columns]
        if missing:
            raise ValueError(f"Missing required variables: {missing}")

    def _compute_pca(self, features_df: pd.DataFrame) -> tuple[pd.DataFrame, PCA]:
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features_df)
        pca = PCA(n_components=features_df.shape[1])
        principal_components = pca.fit_transform(features_scaled)
        num_components = principal_components.shape[1]
        pca_cols = [f"PC{i+1}" for i in range(num_components)]
        pca_df = pd.DataFrame(
            data=principal_components,
            columns=pca_cols,
            index=features_df.index,
        )
        return pca_df, pca

    def _fit_predict_kmeans(self, pca_subset: pd.DataFrame) -> pd.Series:
        model = KMeans(
            n_clusters=self.n_clusters,
            random_state=self.random_state,
        )
        labels = model.fit_predict(pca_subset)
        return pd.Series(labels, index=pca_subset.index, name="cluster")

    def _build_result(
        self, recipes: pd.DataFrame, pca_df: pd.DataFrame, clusters: pd.Series
    ) -> pd.DataFrame:
        out = pd.DataFrame(index=recipes.index)
        if "name" in recipes.columns:
            out["name"] = recipes["name"]
        elif "name_x" in recipes.columns:
            out["name"] = recipes["name_x"]
        out["cluster"] = clusters
        out["pc_1"] = pca_df["PC1"]
        out["pc_2"] = pca_df["PC2"]
        return out

    def _save_output(self, df: pd.DataFrame) -> None:
        out_path = self.paths.output_csv()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(out_path, index=True)
