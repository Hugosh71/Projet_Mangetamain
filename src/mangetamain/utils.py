"""Utility functions"""

import logging
from functools import lru_cache

import pandas as pd

logging.basicConfig(level=logging.INFO)


@lru_cache(maxsize=5)
def read_csv(path, usecols: tuple[str, ...] | str | None = None) -> pd.DataFrame:
    """Load a CSV file with caching to optimize repeated reads."""
    logging.info("Loading CSV from %s with usecols=%s", path, usecols)
    return pd.read_csv(path, usecols=list(usecols))
