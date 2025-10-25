from pathlib import Path
import logging
import pandas as pd
from mangetamain.backend import (
    CSVDataRepository,
    ProcessorFactory,
    RepositoryPaths,
)
from mangetamain.backend.rating.analyzers import RatingAnalyser

def test_rating_pipeline_e2e() -> None:
    
    tmp_path = Path("tmp/test_rating_pipeline_e2e")
    tmp_path.mkdir(parents=True, exist_ok=True)
    recipes = pd.DataFrame(
        [
            {"id": 1, "name": "A"},
            {"id": 2, "name": "B"},
        ]
    )
    interactions = pd.DataFrame(
        [
            {"recipe_id": 1, "rating": 0},
            {"recipe_id": 1, "rating": 5},
            {"recipe_id": 2, "rating": 4},
        ]
    )

    recipes_path = tmp_path / "recipes.csv"
    interactions_path = tmp_path / "interactions.csv"
    recipes.to_csv(recipes_path, index=False)
    interactions.to_csv(interactions_path, index=False)

    # recipes_path = "data/RAW_recipes.csv"
    # interactions_path = "data/RAW_interactions.csv"

    repo = CSVDataRepository(
        paths=RepositoryPaths(
            recipes_csv=str(recipes_path),
            interactions_csv=str(interactions_path),
        ),
        recipe_usecols=["id", "name"],
        interaction_usecols=["recipe_id", "rating"],
        logger=logging.getLogger("test_rating_pipeline"),
    )

    processor = ProcessorFactory.create_rating(repo)
    processed = processor.run()

    analyser = RatingAnalyser()
    result = analyser.analyze(
        processed.recipes,
        processed.interactions, 
    )

    assert not result.table.empty
    report = analyser.generate_report(result, tmp_path / "test_rating_pipeline_e2e.csv")
    assert Path(report["path"]).exists()
