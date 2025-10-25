"""Repository implementations for loading raw data."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import pandas as pd

from .exceptions import DataLoadError, DataNotFoundError
from .interfaces import IDataRepository


@dataclass(frozen=True)
class RepositoryPaths:
    """Filesystem locations for raw CSV inputs."""

    recipes_csv: str = "data/RAW_recipes.csv"
    interactions_csv: str = "data/RAW_interactions.csv"


class CSVDataRepository(IDataRepository):
    """Load dataframes from CSV files with optional column selection."""

    def __init__(
        self,
        paths: RepositoryPaths | None = None,
        *,
        recipe_usecols: Sequence[str] | None = ("id", "name"),
        interaction_usecols: Sequence[str] | None = ("recipe_id"),
        logger: logging.Logger | None = None,
    ) -> None:
        self._paths = paths or RepositoryPaths()
        self._recipe_usecols = list(recipe_usecols) if recipe_usecols else None
        self._interaction_usecols = (
            list(interaction_usecols) if interaction_usecols else None
        )
        self._logger = logger or logging.getLogger("mangetamain.backend.repo")

    def _ensure_exists(self, file_path: str) -> Path:
        path = Path(file_path)
        if not path.exists():
            self._logger.error("Data file not found: %s", path)
            raise DataNotFoundError(str(path))
        return path

    def load_recipes(self) -> pd.DataFrame:
        path = self._ensure_exists(self._paths.recipes_csv)
        try:
            df = pd.read_csv(path, usecols=self._recipe_usecols)
            self._logger.debug("Loaded recipes: %d rows", len(df))
            return df
        except Exception as exc:  # noqa: BLE001 - wrap into domain error
            raise DataLoadError(f"Failed to load recipes from {path}") from exc

    def load_interactions(self) -> pd.DataFrame:
        path = self._ensure_exists(self._paths.interactions_csv)
        try:
            df = pd.read_csv(path, usecols=self._interaction_usecols)
            self._logger.debug("Loaded interactions: %d rows", len(df))
            return df
        except Exception as exc:  # noqa: BLE001 - wrap into domain error
            raise DataLoadError(f"Failed to load interactions from {path}") from exc
