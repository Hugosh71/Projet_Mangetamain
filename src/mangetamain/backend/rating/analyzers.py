"""Analyzers for rating feature."""

from __future__ import annotations

import logging

import pandas as pd

from ..interfaces import Analyser, AnalysisResult


class RatingAnalyser(Analyser):
    """Produce high-level insights for ratings (top-K by mean, etc.)."""

    def __init__(self, *, logger: logging.Logger | None = None) -> None:
        self._logger = logger or logging.getLogger(
            "mangetamain.backend.rating"
        )

    def analyze(
        self,
        recipes: pd.DataFrame,
        interactions: pd.DataFrame,
        *,
        top_k: int = 10,
    ) -> AnalysisResult:
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

    def generate_report(self, result: AnalysisResult) -> dict[str, object]:
        self._logger.debug("Generating rating analysis report payload")
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


