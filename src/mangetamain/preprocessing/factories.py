"""Factories to assemble backend components with sensible defaults."""

from __future__ import annotations

import logging

from .feature.ingredients import IngredientsCleaning, IngredientsPreprocessing
from .feature.nutrition import NutritionCleaning, NutritionPreprocessing
from .feature.rating import RatingCleaning, RatingPreprocessing
from .feature.seasonality import SeasonalityCleaning, SeasonalityPreprocessing
from .feature.steps import StepsCleaning, StepsPreprocessing
from .processors import (
    BasicDataProcessor,
    NoOpCleaning,
    NoOpPreprocessing,
)


class ProcessorFactory:
    """Build preconfigured processors with default strategies."""

    @staticmethod
    def create_basic(
        repository, *, logger: logging.Logger | None = None
    ) -> BasicDataProcessor:
        return BasicDataProcessor(
            repository,
            cleaning=NoOpCleaning(),
            preprocessing=NoOpPreprocessing(),
            logger=logger,
        )

    @staticmethod
    def create_rating(
        repository, *, logger: logging.Logger | None = None
    ) -> BasicDataProcessor:
        return BasicDataProcessor(
            repository,
            cleaning=RatingCleaning(),
            preprocessing=RatingPreprocessing(),
            logger=logger,
        )

    @staticmethod
    def create_seasonality(
        repository, *, logger: logging.Logger | None = None
    ) -> BasicDataProcessor:
        return BasicDataProcessor(
            repository,
            cleaning=SeasonalityCleaning(),
            preprocessing=SeasonalityPreprocessing(),
            logger=logger,
        )

    @staticmethod
    def create_ingredients(
        repository, *, logger: logging.Logger | None = None
    ) -> BasicDataProcessor:
        return BasicDataProcessor(
            repository,
            cleaning=IngredientsCleaning(),
            preprocessing=IngredientsPreprocessing(),
            logger=logger,
        )

    @staticmethod
    def create_nutrition(
        repository, *, logger: logging.Logger | None = None
    ) -> BasicDataProcessor:
        return BasicDataProcessor(
            repository,
            cleaning=NutritionCleaning(),
            preprocessing=NutritionPreprocessing(),
            logger=logger,
        )

    @staticmethod
    def create_steps(
        repository, *, logger: logging.Logger | None = None
    ) -> BasicDataProcessor:
        return BasicDataProcessor(
            repository,
            cleaning=StepsCleaning(),
            preprocessing=StepsPreprocessing(),
            logger=logger,
        )
