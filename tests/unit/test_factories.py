import pandas as pd
from pathlib import Path

from mangetamain.preprocessing.factories import ProcessorFactory
from mangetamain.preprocessing.repositories import (
    CSVDataRepository,
    RepositoryPaths,
)


def test_processor_factory_variants(tmp_path: Path) -> None:
    # Minimal CSVs
    recipes = pd.DataFrame([{"id": 1, "name": "A"}])
    interactions = pd.DataFrame([{"recipe_id": 1, "rating": 5}])
    rp = tmp_path / "r.csv"
    ip = tmp_path / "i.csv"
    recipes.to_csv(rp, index=False)
    interactions.to_csv(ip, index=False)

    repo = CSVDataRepository(
        paths=RepositoryPaths(recipes_csv=str(rp), interactions_csv=str(ip)),
        recipe_usecols=["id", "name"],
        interaction_usecols=["recipe_id", "rating"],
    )

    for maker in (
        ProcessorFactory.create_basic,
        ProcessorFactory.create_rating,
        ProcessorFactory.create_seasonality,
        ProcessorFactory.create_ingredients,
        ProcessorFactory.create_nutrition,
        ProcessorFactory.create_steps,
    ):
        processor = maker(repo)
        out = processor.run()
        assert set(out.recipes.columns) >= {"id", "name"}

