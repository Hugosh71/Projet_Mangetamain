"""Seasonality analysers (stubs)."""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd

from ...interfaces import Analyser, AnalysisResult


class SeasonalityAnalyzer(Analyser):
    def __init__(self, *, logger: logging.Logger | None = None) -> None:
        self._logger = logger or logging.getLogger(__name__)

    def analyze(
        self,
        recipes: pd.DataFrame,
        interactions: pd.DataFrame,
        **kwargs: object,
    ) -> AnalysisResult:
        self._logger.debug(
            "Computing seasonality features for recipes based on user interaction data"
        )

        df_interactions = interactions.copy()
        date_col = "date"
        group_col = "recipe_id"
        k = 5.0

        # Validate required columns
        if (
            date_col not in df_interactions.columns
            or group_col not in df_interactions.columns
        ):
            raise ValueError(
                f"interactions must contain '{date_col}' and '{group_col}'"
            )

        # Convert date column to datetime and compute day-of-year
        df_interactions[date_col] = pd.to_datetime(
            df_interactions[date_col], errors="coerce"
        )
        if df_interactions[date_col].isna().any():
            raise ValueError(f"Invalid dates found in '{date_col}'")

        doy = df_interactions[date_col].dt.dayofyear
        df_interactions["doy_sin"] = np.sin(2 * np.pi * doy / 365)
        df_interactions["doy_cos"] = np.cos(2 * np.pi * doy / 365)

        # Compute global sine/cosine averages for smoothing
        sin_global_ = df_interactions["doy_sin"].mean()
        cos_global_ = df_interactions["doy_cos"].mean()

        # Aggregate per recipe_id
        agg = (
            df_interactions.groupby(group_col)
            .agg(
                sin_mean=("doy_sin", "mean"),
                cos_mean=("doy_cos", "mean"),
                n=("doy_sin", "size"),
            )
            .reset_index()
        )

        # Empirical Bayes smoothing
        agg["inter_doy_sin_smooth"] = (agg["n"] * agg["sin_mean"] + k * sin_global_) / (
            agg["n"] + k
        )

        agg["inter_doy_cos_smooth"] = (agg["n"] * agg["cos_mean"] + k * cos_global_) / (
            agg["n"] + k
        )

        # Compute seasonal strength (vector length)
        agg["inter_strength"] = np.sqrt(
            agg["inter_doy_sin_smooth"] ** 2 + agg["inter_doy_cos_smooth"] ** 2
        )

        # Store only the aggregated features for merging later
        df_features = agg[
            [
                group_col,
                "inter_doy_sin_smooth",
                "inter_doy_cos_smooth",
                "inter_strength",
            ]
        ]

        return AnalysisResult(table=df_features, summary={})

    def generate_report(self, result: AnalysisResult, path):
        self._logger.debug("Writing seasonality_table.csv and seasonality_summary.csv")

        path = Path(path)
        if path.is_dir():
            out_table = path / "seasonality_table.csv"
            out_summary = path / "seasonality_summary.csv"
        else:
            # If a file path is passed, use its parent directory
            out_table = path.parent / "seasonality_table.csv"
            out_summary = path.parent / "seasonality_summary.csv"

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
