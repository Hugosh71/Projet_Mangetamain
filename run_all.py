from __future__ import annotations

import logging
from pathlib import Path

import numpy as np

from src.app.logging_config import configure_logging, get_logger
from src.mangetamain.clustering import RecipeClusteringPipeline
from src.mangetamain.clustering import ClusteringPaths as ClusPaths
from src.mangetamain.preprocessing.factories import ProcessorFactory
from src.mangetamain.preprocessing.feature.ingredients import (
    IngredientsAnalyser,
)
from src.mangetamain.preprocessing.feature.nutrition import (
    NutritionAnalyser,
)
from src.mangetamain.preprocessing.feature.rating import RatingAnalyser
from src.mangetamain.preprocessing.feature.seasonality import (
    SeasonalityAnalyzer,
)
from src.mangetamain.preprocessing.feature.steps import StepsAnalyser
from src.mangetamain.preprocessing.repositories import (
    CSVDataRepository,
    RepositoryPaths,
)


def ensure_dirs() -> None:
    Path("data/preprocessed").mkdir(parents=True, exist_ok=True)
    Path("data/clustering").mkdir(parents=True, exist_ok=True)
    Path("logs").mkdir(parents=True, exist_ok=True)


def run_preprocessing(logger: logging.Logger) -> dict[str, Path]:
    """Generate and save required preprocessed CSVs.

    Returns a mapping from logical name to generated CSV path under
    data/preprocessed/.
    """
    repo = CSVDataRepository(paths=RepositoryPaths())

    outputs: dict[str, Path] = {}

    # Rating features
    logger.info("Preprocessing: rating features …")
    proc_rating = ProcessorFactory.create_rating(repo, logger=logger)
    pair_rating = proc_rating.run()
    rating_an = RatingAnalyser(logger=logger)
    rating_result = rating_an.analyze(
        pair_rating.recipes, pair_rating.interactions
    )
    # Align notebook naming and index
    rating_df = (
        rating_result.table.rename(columns={
            "recipe_id": "id",
            "mean_rating": "rating_mean",
        })
        .set_index("id", drop=True)
    )
    rating_path = Path("data/preprocessed/recipes_feature_rating_full.csv")
    rating_df.to_csv(rating_path)
    outputs["rating"] = rating_path

    # Seasonality features
    logger.info("Preprocessing: seasonality features …")
    proc_season = ProcessorFactory.create_seasonality(repo, logger=logger)
    pair_season = proc_season.run()
    season_an = SeasonalityAnalyzer(logger=logger)
    season_result = season_an.analyze(
        pair_season.recipes, pair_season.interactions
    )
    season_df = (
        season_result.table.rename(columns={"recipe_id": "id"})
        .set_index("id", drop=True)
    )
    season_path = Path("data/preprocessed/recipe_seasonality_features.csv")
    season_df.to_csv(season_path)
    outputs["seasonality"] = season_path

    # Nutrition features (placeholder: pass-through recipes)
    logger.info("Preprocessing: nutrition features …")
    proc_nutri = ProcessorFactory.create_nutrition(repo, logger=logger)
    pair_nutri = proc_nutri.run()
    nutri_an = NutritionAnalyser()
    nutri_result = nutri_an.analyze(
        pair_nutri.recipes, pair_nutri.interactions
    )
    # Expect nutrition output to already contain required nutrition columns
    nutri_df = nutri_result.table.set_index("id", drop=True)
    # As in the notebook, nutrition CSV uses ';' and has index in first column
    nutri_path = Path("data/preprocessed/features_nutrition.csv")
    nutri_df.to_csv(nutri_path, sep=";")
    outputs["nutrition"] = nutri_path

    # Steps/complexity features (placeholder): we compute z-scores if present
    logger.info("Preprocessing: complexity features …")
    proc_steps = ProcessorFactory.create_steps(repo, logger=logger)
    pair_steps = proc_steps.run()
    steps_an = StepsAnalyser()
    steps_result = steps_an.analyze(
        pair_steps.recipes, pair_steps.interactions
    )
    steps_df = steps_result.table.copy()
    if {"n_steps", "n_ingredients", "minutes"}.issubset(steps_df.columns):
        # Simple z-scores for required features
        for col, out in (
            ("n_steps", "n_steps_z"),
            ("n_ingredients", "n_ingredients_z"),
        ):
            s = steps_df[col].astype(float)
            steps_df[out] = (s - s.mean()) / (s.std(ddof=0) or 1.0)
        # minutes_log from minutes
        steps_df["minutes_log"] = (
            steps_df["minutes"].astype(float) + 1
        ).apply(lambda x: np.log(x))
    steps_df = steps_df.rename(columns={"id": "id"}).set_index("id", drop=True)
    comp_path = Path("data/preprocessed/recipes_features_complexity.csv")
    steps_df.to_csv(comp_path)
    outputs["complexity"] = comp_path

    # Ingredients axes features (placeholder: pass-through if exist)
    logger.info("Preprocessing: ingredients axes …")
    proc_ing = ProcessorFactory.create_ingredients(repo, logger=logger)
    pair_ing = proc_ing.run()
    ing_an = IngredientsAnalyser()
    ing_result = ing_an.analyze(pair_ing.recipes, pair_ing.interactions)
    ing_df = ing_result.table.set_index("id", drop=True)
    ing_path = Path("data/preprocessed/features_axes_ingredients.csv")
    ing_df.to_csv(ing_path)
    outputs["ingredients"] = ing_path

    logger.info("Preprocessing done")
    return outputs


def run_clustering(logger: logging.Logger) -> Path:
    logger.info("Clustering + PCA …")
    pipeline = RecipeClusteringPipeline(paths=ClusPaths())
    df = pipeline.run()
    out_path = ClusPaths().output_csv()
    logger.info(
        "Clustering done → %s (%d rows)", out_path, len(df)
    )
    return out_path


def upload_to_s3_stub(csv_path: Path, logger: logging.Logger) -> None:
    # Placeholder for S3 upload logic
    logger.info("[stub] Would upload %s to S3 (simulate)", csv_path)
    print(f"[stub] upload to S3: {csv_path}")


def main() -> None:
    ensure_dirs()
    configure_logging(log_directory="./logs", reset_existing=True)
    logger = get_logger("runner")

    logger.info("Starting end-to-end pipeline")
    run_preprocessing(logger)
    out_csv = run_clustering(logger)
    upload_to_s3_stub(out_csv, logger)
    logger.info("Pipeline completed successfully")


if __name__ == "__main__":
    main()

