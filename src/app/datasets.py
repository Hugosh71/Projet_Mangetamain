from __future__ import annotations

import logging
import shutil
from pathlib import Path


def _find_file(root: Path, name: str) -> Path | None:
    for p in root.rglob(name):
        if p.is_file():
            return p
    return None


def run_downloading_datasets(logger: logging.Logger | None = None) -> dict[str, Path]:
    """Download Food.com dataset via kagglehub and place RAW CSVs under data/.

    Returns a mapping with keys 'recipes' and 'interactions' pointing to
    destination paths in ./data.
    """
    log = logger or logging.getLogger("app.datasets")
    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)

    dest_recipes = data_dir / "RAW_recipes.csv"
    dest_interactions = data_dir / "RAW_interactions.csv"

    if dest_recipes.exists() and dest_interactions.exists():
        log.info("RAW CSVs already present; skipping download")
        return {"recipes": dest_recipes, "interactions": dest_interactions}

    try:
        import kagglehub  # type: ignore
    except Exception as exc:  # pragma: no cover - optional dep
        log.error("kagglehub not available: %s", exc)
        raise

    log.info(
        "Downloading Kaggle dataset shuyangli94/food-com-recipes-and-user-interactions"
    )
    root_path_str = kagglehub.dataset_download(  # type: ignore[name-defined]
        "shuyangli94/food-com-recipes-and-user-interactions"
    )
    src_root = Path(root_path_str)
    log.debug("Dataset downloaded to %s", src_root)

    src_recipes = _find_file(src_root, "RAW_recipes.csv")
    src_interactions = _find_file(src_root, "RAW_interactions.csv")
    if not src_recipes or not src_interactions:
        raise FileNotFoundError("RAW_recipes.csv or RAW_interactions.csv not found")

    shutil.copy2(src_recipes, dest_recipes)
    shutil.copy2(src_interactions, dest_interactions)
    log.info("Copied RAW CSVs into %s", data_dir)
    return {"recipes": dest_recipes, "interactions": dest_interactions}
