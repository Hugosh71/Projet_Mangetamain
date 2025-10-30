"""Steps analysers.

This module provides tools to compute and report recipe complexity
features based on preparation steps, ingredients, and cooking time.
It standardizes recipe attributes, derives categorical complexity
clusters, and produces summary statistics for reporting.

The goal is to quantify recipe complexity in a consistent, scalable way,
useful for recommendation models or descriptive analytics.
"""

from __future__ import annotations

import logging
from pathlib import Path


import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

from ...interfaces import Analyser, AnalysisResult


class StepsAnalyser(Analyser):
    """Analyzes recipe complexity based on steps, ingredients, and cooking time.

    This analyzer computes standardized and categorical representations
    of recipe complexity. It standardizes key numeric attributes (e.g.,
    number of steps, number of ingredients, preparation time), applies
    logarithmic transformation to duration, and groups recipes into
    interpretable complexity clusters.

    It produces both a per-recipe feature table and a summary report of
    global statistics such as mean steps, mean ingredients, and the
    correlation between them.
    """
    def __init__(self, *, logger: logging.Logger | None = None) -> None:
        self._logger = logger or logging.getLogger(__name__)
    """Initializes the StepsAnalyser.

        Args:
            logger (logging.Logger | None): Optional custom logger instance.
                If not provided, a module-level logger will be used.
        """

    def analyze(
        self,
        recipes: pd.DataFrame,
        interactions: pd.DataFrame,
        **kwargs: object,
    ) -> AnalysisResult:
        """Computes recipe complexity features based on step and ingredient counts.

        The method standardizes numeric columns (`minutes`, `n_steps`,
        `n_ingredients`) using z-scores, applies a logarithmic
        transformation to `minutes`, and derives complexity clusters
        combining step and ingredient categories. It also computes global
        descriptive statistics for reporting.

        Args:
            recipes (pd.DataFrame): DataFrame containing recipe metadata with
                required columns:
                - ``minutes`` (float): Total preparation time.
                - ``n_steps`` (int): Number of procedural steps.
                - ``n_ingredients`` (int): Number of unique ingredients.
            interactions (pd.DataFrame): Unused placeholder for interface
                compatibility.
            **kwargs (object): Additional keyword arguments (unused).

        Returns:
            AnalysisResult: Object containing:
                - ``table`` (pd.DataFrame): Per-recipe complexity features:
                  ['id', 'minutes', 'n_steps', 'n_ingredients', 'minutes_z',
                   'n_steps_z', 'n_ingredients_z', 'minutes_log',
                   'cluster_ing_steps', 'cluster_label_ing_steps']
                - ``summary`` (dict): Aggregated metrics including:
                  - 'moyenne_etapes'
                  - 'moyenne_ingredients'
                  - 'correlation_steps_ingredients'
                  - 'nb_clusters'

        Raises:
            ValueError: If any of the required columns is missing.
        """
        self._logger.debug("Analyzing recipe complexity by steps and ingredients")
        df = recipes.copy()

        # Vérification colonnes obligatoires
        required_cols = ["minutes", "n_steps", "n_ingredients"]
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")

        # Transformation logarithmique sur le temps (pour réduire l’effet des valeurs extrêmes)
        df["minutes_log"] = np.log1p(df["minutes"])  # log(1 + x)

        # Standardisation : moyenne = 0, écart-type = 1
        cols_to_scale = ["minutes", "n_steps", "n_ingredients"]
        scaler = StandardScaler()
        scaled_values = scaler.fit_transform(df[cols_to_scale])

        # Ajout des colonnes standardisées
        for i, col in enumerate(cols_to_scale):
            df[f"{col}_z"] = scaled_values[:, i]

        # Catégorisation selon n_steps et n_ingredients
        df["n_steps_cat"] = pd.qcut(df["n_steps_z"], 3, labels=[0, 1, 2])
        df["n_ingredients_cat"] = pd.qcut(df["n_ingredients_z"], 3, labels=[0, 1, 2])

        # Création du cluster brut
        df["cluster_ing_steps"] = (
            df["n_steps_cat"].astype(str) + "_" + df["n_ingredients_cat"].astype(str)
        )

        # Ajout d’un libellé lisible pour les clusters (aligné avec le notebook EDA)
        cluster_label_map = {
            '0_0': 'simple faible',
            '0_1': 'simple moyen',
            '0_2': 'simple élevé',
            '1_0': 'intermédiaire faible',
            '1_1': 'intermédiaire moyen',
            '1_2': 'intermédiaire élevé',
            '2_0': 'complexe faible',
            '2_1': 'complexe moyen',
            '2_2': 'complexe élevé',
        }

        df["cluster_label_ing_steps"] = df["cluster_ing_steps"].map(cluster_label_map)

        # Résumé global
        summary = {
            "moyenne_etapes": df["n_steps"].mean(),
            "moyenne_ingredients": df["n_ingredients"].mean(),
            "correlation_steps_ingredients": df["n_steps"].corr(df["n_ingredients"]),
            "nb_clusters": df["cluster_ing_steps"].nunique(),
        }

        # Table finale avec les colonnes demandées
        if "id" not in df.columns:
            df = df.reset_index().rename(columns={"index": "id"})
        final_cols = [
            "id",
            "minutes",
            "n_steps",
            "n_ingredients",
            "minutes_z",
            "n_steps_z",
            "n_ingredients_z",
            "minutes_log",
            "cluster_ing_steps",
            "cluster_label_ing_steps",
        ]
        result_table = df[final_cols].copy()
        return AnalysisResult(table=result_table, summary=summary)

    def generate_report(self, result: AnalysisResult, path: Path | str) -> dict[str, object]:
        """Génère les fichiers de rapport pour l'analyse des étapes."""
        self._logger.debug("Writing steps_analysis.csv and steps_summary.csv")

        path = Path(path)
        if path.is_dir():
            # Table name aligned with EDA notebook export
            out_table = path / "recipes_features_cngy.csv"
            out_summary = path / "recipes_features_cngy_summary.csv"
        else:
            # If a file path is passed, use its parent directory
            out_table = path.parent / "recipes_features_cngy.csv"
            out_summary = path.parent / "recipes_features_cngy_summary.csv"

        # Create parent directory if it doesn't exist
        out_table.parent.mkdir(parents=True, exist_ok=True)

        # Write detailed per-recipe table
        result.table.to_csv(out_table, index=False)

        # Write summary as key,value rows
        summary_df = pd.DataFrame([result.summary]).melt(
            var_name="metric", value_name="value"
        )
        summary_df.to_csv(out_summary, index=False)

        return {
            "table_path": str(out_table),
            "summary_path": str(out_summary),
        }