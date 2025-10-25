"""Abstract interfaces and strategies for backend processing."""

from __future__ import annotations

import abc
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import pandas as pd


class IDataRepository(abc.ABC):
    """Abstraction for loading raw dataframes from a data source."""

    @abc.abstractmethod
    def load_recipes(self) -> pd.DataFrame:  # pragma: no cover
        """Return the raw recipes dataframe."""

    @abc.abstractmethod
    def load_interactions(
        self,
    ) -> pd.DataFrame:  # pragma: no cover
        """Return the raw interactions dataframe."""


class IValidator(abc.ABC):
    """Validation contract applied to dataframes before processing."""

    @abc.abstractmethod
    def validate(self, df: pd.DataFrame) -> None:  # pragma: no cover
        """Raise on invalid dataframe; return None on success."""


class ICleaningStrategy(Protocol):
    """Strategy to clean raw dataframes prior to preprocessing."""

    def clean(
        self, recipes: pd.DataFrame, interactions: pd.DataFrame
    ) -> tuple[pd.DataFrame, pd.DataFrame]:  # pragma: no cover - protocol only
        ...


class IPreprocessingStrategy(Protocol):
    """Strategy to transform cleaned dataframes into model-ready form."""

    def preprocess(
        self, recipes: pd.DataFrame, interactions: pd.DataFrame
    ) -> tuple[pd.DataFrame, pd.DataFrame]:  # pragma: no cover - protocol only
        ...


@dataclass(frozen=True)
class ProcessedPair:
    """Container for a pair of dataframes used across the pipeline."""

    recipes: pd.DataFrame
    interactions: pd.DataFrame


@dataclass(frozen=True)
class AnalysisResult:
    """Container for analyzer outputs shared across implementations."""

    # Single detailed table with all per-recipe metrics
    table: pd.DataFrame
    # Global summary metrics
    summary: dict[str, object]


class Analyser(abc.ABC):
    """Abstract base for domain analyzers (rating, ingredients, steps, …)."""

    @abc.abstractmethod
    def analyze(
        self,
        recipes: pd.DataFrame,
        interactions: pd.DataFrame,
        **kwargs: object,
    ) -> AnalysisResult:  # pragma: no cover - interface only
        """Produce analysis artefacts from processed dataframes."""

    @abc.abstractmethod
    def generate_report(
        self, result: AnalysisResult, path: Path
    ) -> dict[str, object]:  # pragma: no cover - interface only
        """Return a minimal, serializable representation of the result."""


class DataProcessor(abc.ABC):
    """Abstract processor defining the high-level pipeline steps.

    Subclasses typically orchestrate a repository and strategies to
    implement ``clean`` and ``preprocess`` while exposing a ``run`` helper.
    """

    def __init__(
        self,
        repository: IDataRepository,
        *,
        logger: logging.Logger | None = None,
    ) -> None:
        self._repository = repository
        self._logger = logger or logging.getLogger("mangetamain.data_processing")

    @abc.abstractmethod
    def clean(
        self, recipes: pd.DataFrame, interactions: pd.DataFrame
    ) -> ProcessedPair:  # pragma: no cover - interface only
        """Return cleaned dataframes."""

    @abc.abstractmethod
    def preprocess(
        self, recipes: pd.DataFrame, interactions: pd.DataFrame
    ) -> ProcessedPair:  # pragma: no cover - interface only
        """Return preprocessed dataframes."""

    def run(self) -> ProcessedPair:
        """Load, clean, and preprocess data in sequence."""
        self._logger.debug("Loading raw dataframes from repository")
        recipes = self._repository.load_recipes()
        interactions = self._repository.load_interactions()

        self._logger.debug("Cleaning dataframes")
        cleaned = self.clean(recipes, interactions)

        self._logger.debug("Preprocessing dataframes")
        preprocessed = self.preprocess(cleaned.recipes, cleaned.interactions)
        return preprocessed
