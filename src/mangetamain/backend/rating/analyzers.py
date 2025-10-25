"""Analyzers for rating feature."""

from __future__ import annotations

import logging
from pathlib import Path
import pandas as pd

from ..interfaces import Analyser, AnalysisResult


class RatingAnalyser(Analyser):
    """Produce high-level insights for ratings (top-K by mean, etc.)."""

    def __init__(self, *, logger: logging.Logger | None = None) -> None:
        self._logger = logger or logging.getLogger("mangetamain.backend.rating")

    def analyze(
        self,
        recipes: pd.DataFrame,
        interactions: pd.DataFrame,
        *,
        c: int | None = None,
        mu_percentile: float = 0.5,
        include_zero_ratings: bool = True,
        with_wilson_per_recipe: bool = False,
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
        rating_series = interactions["rating"].astype(float)
        is_rated = rating_series.fillna(0) > 0

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
            rated_agg = (
                rated_grp["rating"]
                .agg(
                    mean_rating="mean",
                    median_rating="median",
                    rating_std="std",
                )
                .reset_index()
                .fillna({"rating_std": 0})
            )

        # Attach recipe names
        # rated_agg = rated_agg.merge(
        #     per_recipe.merge(
        #         recipes[["id", "name"]],
        #         left_on="recipe_id",
        #         right_on="id",
        #         how="left",
        #     )
        #     .drop(columns=["id"])
        #     .rename(columns={"name": "recipe_name"})
        # )

        # Merge aggregates
        per_recipe = n_interactions.merge(n_rated, on="recipe_id", how="left").merge(
            rated_agg, on="recipe_id", how="left"
        )
        per_recipe["n_rated"] = per_recipe["n_rated"].fillna(0).astype(int)
        per_recipe["share_rated"] = (
            per_recipe["n_rated"].divide(per_recipe["n_interactions"]).fillna(0)
        )

        # Bayesian smoothing (simple):
        # bayes_mean = (mu * c + sum_ratings) / (c + n_rated)
        # Choose c as global prior strength; mu as global mean over rated
        # Informative prior mean based on percentile of rated-only distribution
        mu = (
            float(rated_only["rating"].quantile(mu_percentile))
            if not rated_only.empty
            else 0.0
        )
        c_value = (
            c if c is not None else max(5, int(per_recipe["n_rated"].median() or 5))
        )
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
        per_recipe = per_recipe.merge(sum_ratings, on="recipe_id", how="left").fillna(
            {"sum_ratings": 0.0}
        )
        per_recipe["bayes_mean"] = (mu * c_value + per_recipe["sum_ratings"]) / (
            c_value + per_recipe["n_rated"].clip(lower=0)
        )

        # Additional dispersion metrics
        # if not rated_only.empty:
        #     iqr = (
        #         rated_only.groupby("recipe_id")["rating"].quantile(0.75)
        #         - rated_only.groupby("recipe_id")["rating"].quantile(0.25)
        #     ).rename("iqr_rating").reset_index()
        #     per_recipe = per_recipe.merge(iqr, on="recipe_id", how="left")
        #     per_recipe["cv_rating"] = (
        #         per_recipe["rating_std"] / per_recipe["mean_rating"]
        #     ).replace([pd.NA, pd.NaT], 0).fillna(0)
        # else:
        #     per_recipe["iqr_rating"] = 0.0
        #     per_recipe["cv_rating"] = 0.0

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

        # Optional Wilson bounds per recipe on the proportion of rated interactions
        if with_wilson_per_recipe:
            z = 1.96
            p = per_recipe["share_rated"].fillna(0).astype(float)
            n = per_recipe["n_interactions"].clip(lower=1).astype(float)
            denom = 1 + (z**2) / n
            center = p + (z**2) / (2 * n)
            rad = z * (((p * (1 - p) + (z**2) / (4 * n)) / n)).pow(0.5)
            per_recipe["wilson_low_rec"] = (center - rad) / denom
            per_recipe["wilson_high_rec"] = (center + rad) / denom

        # Global summary only (distribution can be derived downstream if needed)

        # Example global stats (can be extended):
        num_recipes = int(per_recipe["recipe_id"].nunique())
        n_with_rating = int((per_recipe["n_rated"] > 0).sum())
        phat = (per_recipe["n_rated"] / per_recipe["n_interactions"]).fillna(0)
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
            table=per_recipe,
            summary=summary,
        )

    def generate_report(self, result: AnalysisResult, path: Path) -> dict[str, object]:
        self._logger.debug("Writing rating_table.csv and rating_summary.csv")

        path = Path(path)
        if path.is_dir():
            out_table = path / "rating_table.csv"
            out_summary = path / "rating_summary.csv"
        else:
            # If a file path is passed, use its parent directory
            out_table = path.parent / "rating_table.csv"
            out_summary = path.parent / "rating_summary.csv"

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
