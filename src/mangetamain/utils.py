"""Utility functions"""

from functools import lru_cache

import pandas as pd


@lru_cache(maxsize=5)
def read_csv(path, sep=",", nrows=None):
    """Load a CSV file with caching to optimize repeated reads."""
    return pd.read_csv(path, sep=sep, nrows=nrows)
