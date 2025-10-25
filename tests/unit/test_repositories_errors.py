import pandas as pd
import pytest
from pathlib import Path

from mangetamain.preprocessing import (
    CSVDataRepository,
    RepositoryPaths,
)
from mangetamain.preprocessing.exceptions import DataNotFoundError, DataLoadError


def test_repository_ensure_exists_missing(tmp_path: Path) -> None:
    missing_path = tmp_path / "does_not_exist.csv"
    repo = CSVDataRepository(
        paths=RepositoryPaths(
            recipes_csv=str(missing_path),
            interactions_csv=str(missing_path),
        )
    )

    with pytest.raises(DataNotFoundError):
        repo.load_recipes()

    with pytest.raises(DataNotFoundError):
        repo.load_interactions()


def test_repository_load_exceptions_bad_usecols(tmp_path: Path) -> None:
    # Create valid CSV files
    recipes = pd.DataFrame([{"id": 1, "name": "A"}])
    interactions = pd.DataFrame([{"recipe_id": 1, "rating": 5}])
    recipes_path = tmp_path / "recipes.csv"
    interactions_path = tmp_path / "interactions.csv"
    recipes.to_csv(recipes_path, index=False)
    interactions.to_csv(interactions_path, index=False)

    # Configure repository with invalid usecols to trigger read errors
    repo = CSVDataRepository(
        paths=RepositoryPaths(
            recipes_csv=str(recipes_path), interactions_csv=str(interactions_path)
        ),
        recipe_usecols=["nope"],
        interaction_usecols=["nope"],
    )

    with pytest.raises(DataLoadError):
        repo.load_recipes()

    with pytest.raises(DataLoadError):
        repo.load_interactions()


