from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    # Ensure `src` is on sys.path when running as `python src/app/run_all.py`
    sys.path.insert(0, str(ROOT))

import logging  # noqa: E402

import pandas as pd  # noqa: E402

from app.datasets import run_downloading_datasets  # noqa: E402
from app.logging_config import configure_logging, get_logger  # noqa: E402
from mangetamain.clustering import (  # noqa: E402
    ClusteringPaths,
    RecipeClusteringPipeline,
)
from mangetamain.preprocessing.factories import ProcessorFactory  # noqa: E402
from mangetamain.preprocessing.feature.ingredients import (  # noqa: E402
    IngredientsAnalyser,
)
from mangetamain.preprocessing.feature.nutrition import (  # noqa: E402
    NutritionAnalyser,
)
from mangetamain.preprocessing.feature.rating import (  # noqa: E402
    RatingAnalyser,
)
from mangetamain.preprocessing.feature.seasonality import (  # noqa: E402
    SeasonalityAnalyzer,
)
from mangetamain.preprocessing.feature.steps import StepsAnalyser  # noqa: E402
from mangetamain.preprocessing.repositories import (  # noqa: E402
    CSVDataRepository,
    RepositoryPaths,
)


def ensure_dirs() -> None:
    Path("data/preprocessed").mkdir(parents=True, exist_ok=True)
    Path("data/clustering").mkdir(parents=True, exist_ok=True)
    Path("logs").mkdir(parents=True, exist_ok=True)


def _safe_log(logger: logging.Logger, level: int, msg: str, *args) -> None:
    try:
        logger.log(level, msg, *args)
    except Exception:
        pass


def run_preprocessing(logger: logging.Logger) -> dict[str, Path]:
    """Generate and save required preprocessed CSVs via generate_report.

    Returns mapping of logical names to produced file paths.
    """
    repo = CSVDataRepository(paths=RepositoryPaths())
    outputs: dict[str, Path] = {}

    # Rating
    _safe_log(logger, logging.INFO, "Preprocessing: rating …")
    proc_rating = ProcessorFactory.create_rating(repo, logger=logger)
    pair_rating = proc_rating.run()
    rating_an = RatingAnalyser(logger=logger)
    rating_result = rating_an.analyze(
        pair_rating.recipes,
        pair_rating.interactions,
    )
    rating_paths = rating_an.generate_report(
        rating_result,
        Path("data/preprocessed"),
    )
    if isinstance(rating_paths, dict):
        outputs["rating"] = Path(rating_paths["table_path"])
    else:
        outputs["rating"] = Path(
            "data/preprocessed/backup/recipes_feature_rating_full.csv"
        )

    # Seasonality
    _safe_log(logger, logging.INFO, "Preprocessing: seasonality …")
    proc_season = ProcessorFactory.create_seasonality(repo, logger=logger)
    pair_season = proc_season.run()
    season_an = SeasonalityAnalyzer(logger=logger)
    season_result = season_an.analyze(
        pair_season.recipes,
        pair_season.interactions,
    )
    season_paths = season_an.generate_report(
        season_result,
        Path("data/preprocessed"),
    )
    if isinstance(season_paths, dict):
        outputs["seasonality"] = Path(season_paths["table_path"])
    else:
        outputs["seasonality"] = Path(
            "data/preprocessed/backup/recipe_seasonality_features.csv"
        )

    # Nutrition
    _safe_log(logger, logging.INFO, "Preprocessing: nutrition …")
    proc_nutri = ProcessorFactory.create_nutrition(repo, logger=logger)
    pair_nutri = proc_nutri.run()
    nutri_an = NutritionAnalyser()
    nutri_result = nutri_an.analyze(
        pair_nutri.recipes,
        pair_nutri.interactions,
    )
    nutri_paths = nutri_an.generate_report(
        nutri_result,
        Path("data/preprocessed"),
    )
    if isinstance(nutri_paths, dict):
        outputs["nutrition"] = Path(nutri_paths["table_path"])
    else:
        outputs["nutrition"] = Path("data/preprocessed/backup/features_nutrition.csv")

    # Complexity (steps)
    _safe_log(logger, logging.INFO, "Preprocessing: complexity …")
    proc_steps = ProcessorFactory.create_steps(repo, logger=logger)
    pair_steps = proc_steps.run()
    steps_an = StepsAnalyser()
    steps_result = steps_an.analyze(
        pair_steps.recipes,
        pair_steps.interactions,
    )
    steps_paths = steps_an.generate_report(
        steps_result,
        Path("data/preprocessed"),
    )
    if isinstance(steps_paths, dict):
        outputs["complexity"] = Path(steps_paths["table_path"])
    else:
        outputs["complexity"] = Path(
            "data/preprocessed/backup/recipes_features_complexity.csv"
        )

    # Ingredients axes
    _safe_log(
        logger,
        logging.INFO,
        "Preprocessing: ingredients axes …",
    )
    proc_ing = ProcessorFactory.create_ingredients(repo, logger=logger)
    pair_ing = proc_ing.run()
    ing_an = IngredientsAnalyser()
    ing_result = ing_an.analyze(
        pair_ing.recipes,
        pair_ing.interactions,
    )
    ing_paths = ing_an.generate_report(
        ing_result,
        Path("data/preprocessed"),
    )
    if isinstance(ing_paths, dict):
        outputs["ingredients"] = Path(ing_paths["table_path"])
    else:
        outputs["ingredients"] = Path(
            "data/preprocessed/backup/features_axes_ingredients.csv"
        )

    _safe_log(logger, logging.INFO, "Preprocessing done")
    return outputs


def run_clustering(logger: logging.Logger) -> Path:
    _safe_log(
        logger,
        logging.INFO,
        "Clustering + PCA …",
    )
    pipeline = RecipeClusteringPipeline(paths=ClusteringPaths())
    df = pipeline.run()
    out_path = ClusteringPaths().output_csv()
    _safe_log(
        logger,
        logging.INFO,
        "Clustering done → %s (%d rows)",
        out_path,
        len(df),
    )
    return out_path


def merge_all_tables(
    logger: logging.Logger,
    preprocessed_paths: dict[str, Path] | None = None,
    clustering_path: Path | None = None,
) -> pd.DataFrame:
    _safe_log(
        logger,
        logging.INFO,
        "Merging preprocessed tables and clustering …",
    )

    if preprocessed_paths is None:
        preprocessed_paths = {
            "nutrition": Path("data/preprocessed/backup/features_nutrition.csv"),
            "seasonality": Path(
                "data/preprocessed/backup/recipe_seasonality_features.csv"
            ),
            "rating": Path("data/preprocessed/backup/recipes_feature_rating_full.csv"),
            "complexity": Path(
                "data/preprocessed/backup/recipes_features_complexity.csv"
            ),
            "ingredients": Path(
                "data/preprocessed/backup/features_axes_ingredients.csv"
            ),
        }

    else:
        if preprocessed_paths["nutrition"] is None:
            preprocessed_paths["nutrition"] = Path(
                "data/preprocessed/backup/features_nutrition.csv"
            )
        if preprocessed_paths["seasonality"] is None:
            preprocessed_paths["seasonality"] = Path(
                "data/preprocessed/backup/recipe_seasonality_features.csv"
            )
        if preprocessed_paths["rating"] is None:
            preprocessed_paths["rating"] = Path(
                "data/preprocessed/backup/recipes_feature_rating_full.csv"
            )
        if preprocessed_paths["complexity"] is None:
            preprocessed_paths["complexity"] = Path(
                "data/preprocessed/backup/recipes_features_complexity.csv"
            )
        if preprocessed_paths["ingredients"] is None:
            preprocessed_paths["ingredients"] = Path(
                "data/preprocessed/backup/features_axes_ingredients.csv"
            )

    if clustering_path is None:
        clustering_path = Path("data/clustering/recipes_clustering_with_pca.csv")

    # Read tables exactly as in notebook
    nutrition = pd.read_csv(
        preprocessed_paths["nutrition"],
        delimiter=(
            ";"
            if preprocessed_paths["nutrition"]
            == Path("data/preprocessed/backup/features_nutrition.csv")
            else None
        ),
        index_col=0,
    )
    seasonal = pd.read_csv(preprocessed_paths["seasonality"], index_col=0)
    rating = pd.read_csv(preprocessed_paths["rating"], index_col=0)
    complexity = pd.read_csv(preprocessed_paths["complexity"], index_col=0)
    ingredients = pd.read_csv(preprocessed_paths["ingredients"], index_col=0)
    clusters = pd.read_csv(clustering_path, index_col=0)

    df = (
        nutrition.merge(seasonal, left_index=True, right_index=True)
        .merge(rating, left_index=True, right_index=True)
        .merge(complexity, left_index=True, right_index=True)
        .merge(ingredients, left_index=True, right_index=True)
        .merge(
            clusters[["cluster", "pc_1", "pc_2"]],
            left_index=True,
            right_index=True,
        )
    )

    # Normalise id for downstream uses
    df = df.reset_index().rename(columns={df.columns[0]: "id"})
    _safe_log(
        logger,
        logging.INFO,
        "Merged rows: %d",
        len(df),
    )
    return df


def save_merged_gzip(df: pd.DataFrame, logger: logging.Logger) -> Path:
    out_path = Path("data/clustering/recipes_merged.csv.gz")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False, compression="gzip")
    _safe_log(logger, logging.INFO, "Saved merged gzip → %s", out_path)
    return out_path


def run_pipeline() -> Path:
    ensure_dirs()
    configure_logging(log_directory="./logs", reset_existing=True)
    logger = get_logger("runner")
    try:
        # Ensure RAW datasets are present
        raw_recipes = Path("data/RAW_recipes.csv")
        raw_interactions = Path("data/RAW_interactions.csv")
        if not (raw_recipes.exists() and raw_interactions.exists()):
            run_downloading_datasets(logger)
        # Run preprocessing
        preprocessed_paths = run_preprocessing(logger)
        # Run clustering
        clustering_path = run_clustering(logger)
        # Merge all tables
        merged = merge_all_tables(
            logger,
            preprocessed_paths=preprocessed_paths,
            clustering_path=clustering_path,
        )
        # Save merged table
        merged_path = save_merged_gzip(merged, logger)
        return merged_path
    except Exception as exc:  # pragma: no cover - top-level guard
        _safe_log(logger, logging.ERROR, "Pipeline failed: %s", exc)
        raise


def main() -> None:
    run_pipeline()


if __name__ == "__main__":
    main()
