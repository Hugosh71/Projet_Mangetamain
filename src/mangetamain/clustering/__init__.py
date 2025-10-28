"""Clustering pipeline for recipe feature space (PCA + KMeans).

This submodule mirrors the structure and conventions used in
``mangetamain.preprocessing`` while implementing the logic from the
``notebooks/EDA_recipes_clustering.ipynb`` notebook.
"""

from .pipeline import (
    REQUIRED_FEATURES,
    ClusteringPaths,
    RecipeClusteringPipeline,
)

__all__ = [
    "RecipeClusteringPipeline",
    "ClusteringPaths",
    "REQUIRED_FEATURES",
]
