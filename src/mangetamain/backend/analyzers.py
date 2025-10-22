"""Concrete analyzers to derive insights from processed data."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict

import pandas as pd


@dataclass(frozen=True)
class AnalysisResult:
    """Container for analysis artefacts."""

    top_recipes: pd.DataFrame
    summary: Dict[str, Any]


class RecipeAnalyzer:
    """Produce high-level insights over recipes and interactions."""

    def __init__(self, *, logger: logging.Logger | None = None) -> None:
        self._logger = logger or logging.getLogger(
            "mangetamain.backend.analyzer"
        )

    def analyze(
        self,
        recipes: pd.DataFrame,
        interactions: pd.DataFrame,
        *,
        top_k: int = 10,
    ) -> AnalysisResult:
        """Compute top-k recipes by mean rating with variability and counts."""
        self._logger.debug("Computing per-recipe rating statistics")
        grouped = (
            interactions.groupby("recipe_id")["rating"]
            .agg(["mean", "std", "count"])
            .fillna({"std": 0})
            .reset_index()
        )
        self._logger.debug("Selecting top %d recipes", top_k)
        top = (
            grouped.sort_values(
                by=["mean", "std", "count"], ascending=[False, True, False]
            )
            .head(top_k)
            .reset_index(drop=True)
        )
        merged = top.merge(
            recipes[["id", "name"]],
            left_on="recipe_id",
            right_on="id",
            how="left",
        ).rename(
            columns={
                "name": "recipe_name",
                "mean": "rating_mean",
                "std": "rating_std",
                "count": "num_ratings",
            }
        )[
            [
                "recipe_name",
                "recipe_id",
                "rating_mean",
                "rating_std",
                "num_ratings",
            ]
        ]

        summary = {
            "num_unique_recipes": int(
                grouped["recipe_id"].nunique()
            ),
            "num_interactions": int(len(interactions)),
        }
        return AnalysisResult(top_recipes=merged, summary=summary)

    def generate_report(
        self, result: AnalysisResult
    ) -> dict[str, Any]:
        """Return a minimal, serializable analysis payload.

        The report is JSON-friendly: dataframes are summarized into
        light-weight previews and metadata.
        """
        self._logger.debug("Generating analysis report payload")
        # Keep the report minimal and JSON-friendly; dataframes are summarized.
        head_rows = result.top_recipes.head(5).to_dict(
            orient="records"
        )
        return {
            "summary": result.summary,
            "top_recipes_preview": head_rows,
            "columns": list(result.top_recipes.columns),
            "total_top_rows": int(
                len(result.top_recipes)
            ),
        }
