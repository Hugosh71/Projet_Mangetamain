"""Analyzers for rating feature."""

from __future__ import annotations

import logging
from pathlib import Path
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
        self._logger.debug(
            "Computing per-recipe rating statistics with extended metrics"
        )

        # Ensure expected columns exist
        if "recipe_id" not in interactions.columns:
            raise ValueError("interactions must contain 'recipe_id'")
        if "rating" not in interactions.columns:
            interactions = interactions.assign(rating=pd.NA)

        # Build masks
        is_rated = interactions["rating"].fillna(0).astype(float) > 0

        # Per-recipe aggregates
        grp = interactions.groupby("recipe_id", dropna=False)

        n_interactions = grp.size().rename("n_interactions").reset_index()
        n_rated = (
            grp["rating"]
            .apply(lambda s: (s.fillna(0).astype(float) > 0).sum())
            .rename("n_rated")
            .reset_index()
        )

        rated_only = interactions.loc[is_rated].copy()
        if rated_only.empty:
            rated_agg = pd.DataFrame(
                {
                    "recipe_id": pd.Series(dtype="int64"),
                    "mean_rating": pd.Series(dtype="float"),
                    "median_rating": pd.Series(dtype="float"),
                    "rating_std": pd.Series(dtype="float"),
                }
            )
        else:
            rated_grp = rated_only.groupby("recipe_id")
            rated_agg = rated_grp["rating"].agg(
                mean_rating="mean",
                median_rating="median",
                rating_std="std",
            ).reset_index().fillna({"rating_std": 0})

        # Merge aggregates
        per_recipe = (
            n_interactions.merge(n_rated, on="recipe_id", how="left")
            .merge(rated_agg, on="recipe_id", how="left")
        )
        per_recipe["n_rated"] = per_recipe["n_rated"].fillna(0).astype(int)
        per_recipe["share_rated"] = (
            per_recipe["n_rated"]
            .divide(per_recipe["n_interactions"])
            .fillna(0)
        )

        # Bayesian smoothing (simple):
        # bayes_mean = (mu * c + sum_ratings) / (c + n_rated)
        # Choose c as global prior strength; mu as global mean over rated
        global_mu = (
            rated_only["rating"].mean() if not rated_only.empty else 0.0
        )
        c = max(5, int(per_recipe["n_rated"].median() or 5))
        # compute sum_ratings per recipe
        if rated_only.empty:
            sum_ratings = pd.DataFrame(
                {"recipe_id": per_recipe["recipe_id"], "sum_ratings": 0.0}
            )
        else:
            sum_ratings = (
                rated_only.groupby("recipe_id")["rating"]
                .sum()
                .rename("sum_ratings")
                .reset_index()
            )
        per_recipe = per_recipe.merge(
            sum_ratings, on="recipe_id", how="left"
        ).fillna({"sum_ratings": 0.0})
        per_recipe["bayes_mean"] = (
            (global_mu * c + per_recipe["sum_ratings"]) /
            (c + per_recipe["n_rated"].clip(lower=0))
        )

        # Attach recipe names
        per_recipe = (
            per_recipe.merge(
                recipes[["id", "name"]],
                left_on="recipe_id",
                right_on="id",
                how="left",
            )
            .drop(columns=["id"])
            .rename(columns={"name": "recipe_name"})
        )

        # Sort to derive top_k
        top = (
            per_recipe.sort_values(
                by=["bayes_mean", "mean_rating", "rating_std", "n_rated"],
                ascending=[False, False, True, False],
            )
            .head(top_k)
            .reset_index(drop=True)
        )

        # Rating table (distribution) and global summary
        rating_table = (
            rated_only["rating"]
            .value_counts(dropna=False)
            .sort_index()
            .rename_axis("rating")
            .reset_index(name="count")
            if not rated_only.empty
            else pd.DataFrame({"rating": [], "count": []})
        )

        # Example global stats (can be extended):
        num_recipes = int(per_recipe["recipe_id"].nunique())
        n_with_rating = int((per_recipe["n_rated"] > 0).sum())
        phat = (
            per_recipe["n_rated"] / per_recipe["n_interactions"]
        ).fillna(0)
        phat_mean = float(phat.mean()) if len(phat) else 0.0

        # Wilson interval over binary "had rating" at recipe level
        # Using standard 95% z=1.96 on per-recipe indicator
        import math

        z = 1.96
        p = phat_mean
        n = max(1, num_recipes)
        denom = 1 + (z**2) / n
        center = p + (z**2) / (2 * n)
        rad = z * math.sqrt((p * (1 - p) + (z**2) / (4 * n)) / n)
        wilson_low = (center - rad) / denom
        wilson_high = (center + rad) / denom

        summary = {
            "num_unique_recipes": num_recipes,
            "num_interactions": int(len(interactions)),
            "n_with_rating": n_with_rating,
            "phat": phat_mean,
            "wilson_low": wilson_low,
            "wilson_high": wilson_high,
        }

        return AnalysisResult(
            per_recipe=per_recipe,
            top_recipes=top,
            table=rating_table,
            summary=summary,
        )

    def generate_report(self, result: AnalysisResult, path: Path) -> dict[str, object]:
        self._logger.debug(
            "Generating consolidated CSV content for rating analysis"
        )

        # Rating table section
        rating_table_df = result.table
        rating_table_df.to_csv(path, index=False)

        return {
            "path": str(path),
        }


