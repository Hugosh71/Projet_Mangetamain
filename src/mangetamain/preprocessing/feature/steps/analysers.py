"""Steps analysers (stubs)."""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

from ...interfaces import Analyser, AnalysisResult


class StepsAnalyser(Analyser):
    def __init__(self, *, logger: logging.Logger | None = None) -> None:
        self._logger = logger or logging.getLogger(__name__)

    def analyze(
        self,
        recipes: pd.DataFrame,
        interactions: pd.DataFrame,
        **kwargs: object,
    ) -> AnalysisResult:
        self._logger.debug("Analyzing recipe complexity by steps and ingredients")
        df = recipes.copy()

        print(df.columns)

        # Vérification colonnes obligatoires
        required_cols = ["minutes", "n_steps", "n_ingredients"]
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")

        # Transformation logarithmique sur le temps (pour réduire l’effet
        # des valeurs extrêmes)
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
            "0_0": "simple faible",
            "0_1": "simple moyen",
            "0_2": "simple élevé",
            "1_0": "intermédiaire faible",
            "1_1": "intermédiaire moyen",
            "1_2": "intermédiaire élevé",
            "2_0": "complexe faible",
            "2_1": "complexe moyen",
            "2_2": "complexe élevé",
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

    def generate_report(
        self, result: AnalysisResult, path: Path | str
    ) -> dict[str, object]:
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
