"""Ingredients analyser module."""

from __future__ import annotations
import ast
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
from sklearn.cluster import AgglomerativeClustering

from ...interfaces import Analyser, AnalysisResult


class IngredientsAnalyser(Analyser):
    """
    Analyser that extracts semantic and PCA-based features from recipe ingredients.

    This class implements the Analyser interface to process a list of recipes.
    It performs two main tasks:
    1.  Semantic Analysis: Computes scores for each recipe along predefined
        semantic axes (e.g., sweet vs. savory) using sentence embeddings.
    2.  Co-occurrence Analysis: Clusters ingredients based on their embeddings,
        builds a co-occurrence matrix, and applies PCA to extract
        principal components as recipe features.

    Attributes
    ----------
    cluster_threshold : float
        Distance threshold used for hierarchical clustering of ingredients.
    n_pca_components : int
        Number of principal components to compute from the co-occurrence matrix.
    embedding_model_name : str
        Name of the SentenceTransformer model used to compute embeddings.
    model : SentenceTransformer
        The loaded SentenceTransformer model instance.
    """

    DEFAULT_CLUSTER_THRESHOLD: float = 0.5
    DEFAULT_N_PCA_COMPONENTS: int = 10
    DEFAULT_MODEL_NAME: str = "all-mpnet-base-v2"

    AXES_PHRASES: Dict[str, Tuple[str, str]] = {
        "sweet_savory": ("sweet dessert flavor", "savory meal flavor"),
        "spicy_mild": ("spicy hot food", "mild gentle flavor"),
        "lowcal_rich": ("low-calorie healthy food", "rich and fatty dish"),
        "vegetarian_meat": ("vegetarian food without meat", "meat-based dish"),
        "solid_liquid": ("solid food", "liquid food or drink"),
        "raw_processed": ("raw natural ingredient", "processed or prepared food"),
        "western_exotic": ("typical western food", "exotic or asian food"),
    }

    def __init__(
        self,
        cluster_threshold: float | None = None,
        n_pca_components: int | None = None,
        embedding_model: str | None = None,
    ) -> None:
        """
        Initialize the IngredientsAnalyser.

        Parameters
        ----------
        cluster_threshold : float, optional
            The distance threshold for the AgglomerativeClustering.
            If None, defaults to `DEFAULT_CLUSTER_THRESHOLD`.
        n_pca_components : int, optional
            The number of components for PCA.
            If None, defaults to `DEFAULT_N_PCA_COMPONENTS`.
        embedding_model : str, optional
            The name of the SentenceTransformer model to load.
            If None, defaults to `DEFAULT_MODEL_NAME`.
        """
        self.cluster_threshold = cluster_threshold or self.DEFAULT_CLUSTER_THRESHOLD
        self.n_pca_components = n_pca_components or self.DEFAULT_N_PCA_COMPONENTS
        self.embedding_model_name = embedding_model or self.DEFAULT_MODEL_NAME
        self.model = SentenceTransformer(self.embedding_model_name)

    # ======================================================
    # Main public method
    # ======================================================

    def analyze(
        self,
        recipes: pd.DataFrame,
        interactions: pd.DataFrame,
        **kwargs: object,
    ) -> AnalysisResult:
        """
        Main analysis pipeline producing semantic and PCA-based features.

        This method executes the full analysis workflow:
        1. Extracts ingredients.
        2. Computes embeddings.
        3. Calculates semantic scores and adds them to recipes.
        4. Clusters ingredients.
        5. Computes co-occurrence PCA and adds dimensions to recipes.

        Parameters
        ----------
        recipes : pd.DataFrame
            DataFrame containing recipe data, must have an 'ingredients' column
            (expected as a string representation of a list).
        interactions : pd.DataFrame
            DataFrame of user interactions. (Note: This parameter is part of the
            interface but not used in this specific analyser).
        **kwargs : object
            Additional keyword arguments (unused, for interface compatibility).

        Returns
        -------
        AnalysisResult
            An object containing a 'table' (DataFrame with recipe IDs and
            new features) and a 'summary' (dict of mean feature values).
        """
        ingredients, ingredients_count = self._extract_ingredients(recipes)
        embeddings = self._compute_embeddings(ingredients)
        scores_df = self._compute_semantic_scores(ingredients, embeddings)

        recipes = self._add_semantic_features(recipes, scores_df)

        ingredients_df = self._cluster_ingredients(ingredients, embeddings, ingredients_count)
        coords, cluster_labels = self._compute_pca_on_cooccurrence(recipes, ingredients_df)

        recipes = self._add_pca_features(recipes, ingredients_df, coords)

        # Ne renvoyer que l'identifiant et les nouvelles features
        feature_cols = [col for col in recipes.columns if col.startswith("score_") or col.startswith("Dim")]
        if "id" in recipes.columns:
            result_table = recipes[["id"] + feature_cols]
        else:
            result_table = recipes[feature_cols]

        # summary
        summary = result_table[1:].mean().to_dict()

        return AnalysisResult(table=result_table, summary=summary)

    # ======================================================
    # Private sub-methods
    # ======================================================

    def _extract_ingredients(self, recipes: pd.DataFrame) -> Tuple[List[str], pd.Series]:
        """
        Extract unique ingredients and their frequencies from the recipes DataFrame.

        Assumes the 'ingredients' column contains string representations of lists
        which are evaluated using `ast.literal_eval`.

        Parameters
        ----------
        recipes : pd.DataFrame
            The input DataFrame with an 'ingredients' column.

        Returns
        -------
        Tuple[List[str], pd.Series]
            A tuple containing:
            - A list of unique ingredient names.
            - A pandas Series mapping ingredient names to their frequency (count).
        """
        ingredients_series = recipes["ingredients"].apply(ast.literal_eval).explode()
        ingredients_count = ingredients_series.value_counts()
        ingredients = pd.unique(ingredients_series).tolist()
        return ingredients, ingredients_count

    def _compute_embeddings(self, ingredients: List[str]) -> np.ndarray:
        """
        Compute embeddings for all ingredients using a sentence transformer.

        Parameters
        ----------
        ingredients : List[str]
            A list of unique ingredient names.

        Returns
        -------
        np.ndarray
            A 2D numpy array where each row is the embedding vector for the
            corresponding ingredient in the input list.
        """
        return self.model.encode(ingredients)

    def _compute_semantic_scores(
        self,
        ingredients: List[str],
        embeddings: np.ndarray
    ) -> pd.DataFrame:
        """
        Compute cosine similarity scores between ingredients and semantic axes.

        This method projects ingredient embeddings onto semantic axes defined
        in `AXES_PHRASES`. Each axis is a vector difference between two
        contrasting phrases (e.g., "sweet" - "savory").

        Parameters
        ----------
        ingredients : List[str]
            List of ingredient names (used as the index for the output DataFrame).
        embeddings : np.ndarray
            The embedding matrix for the ingredients (must match order of `ingredients`).

        Returns
        -------
        pd.DataFrame
            A DataFrame where rows are ingredients and columns are semantic
            axes (e.g., 'sweet_savory'), containing cosine similarity scores.
        """
        axis_vecs = {
            name: self.model.encode(pos) - self.model.encode(neg)
            for name, (pos, neg) in self.AXES_PHRASES.items()
        }

        axis_names = list(axis_vecs.keys())
        axis_matrix = np.stack(list(axis_vecs.values()))

        # Normalisation pour le cosinus
        emb_norm = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        axis_norm = axis_matrix / np.linalg.norm(axis_matrix, axis=1, keepdims=True)

        cos_sim_matrix = np.dot(emb_norm, axis_norm.T)
        scores_df = pd.DataFrame(cos_sim_matrix, index=ingredients, columns=axis_names)
        return scores_df

    def _add_semantic_features(
        self,
        recipes: pd.DataFrame,
        scores_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Add semantic scores to the recipes DataFrame.

        Calculates the average semantic score for each recipe by averaging the
        scores (from `scores_df`) of its constituent ingredients.

        Parameters
        ----------
        recipes : pd.DataFrame
            The main recipes DataFrame.
        scores_df : pd.DataFrame
            DataFrame of scores per ingredient (output of `_compute_semantic_scores`).

        Returns
        -------
        pd.DataFrame
            The `recipes` DataFrame, modified in-place to include new columns
            (e.g., 'score_sweet_savory').
        """
        for axis in scores_df.columns:
            score_map = scores_df[axis].to_dict()
            recipes[f"score_{axis}"] = recipes["ingredients"].apply(
                lambda ingr_list: np.mean(
                    [score_map[i] for i in ast.literal_eval(ingr_list) if i in score_map]
                )
            )
        return recipes

    def _cluster_ingredients(
        self,
        ingredients: List[str],
        embeddings: np.ndarray,
        ingredients_count: pd.Series
    ) -> pd.DataFrame:
        """
        Cluster ingredients based on embeddings to normalize ingredient names.

        This step serves as a **semantic deduplication** process. Given the presence
        of spelling mistakes, superfluous adjectives, singular/plural forms, and
        synonyms in raw ingredient data (e.g., 'fresh onion' vs. 'onions'),
        hierarchical clustering groups near-identical ingredients based on their
        embeddings. This ensures that the subsequent co-occurrence matrix and PCA
        operate on normalized ingredient "concepts" rather than noisy textual variations.

        Uses AgglomerativeClustering with a cosine metric. The label for each
        cluster is determined by the most frequent ingredient within that cluster.

        Parameters
        ----------
        ingredients : List[str]
            List of unique ingredient names.
        embeddings : np.ndarray
            The embedding matrix for the ingredients.
        ingredients_count : pd.Series
            A Series mapping ingredient names to their frequency, used to
            select the cluster label (most frequent ingredient).

        Returns
        -------
        pd.DataFrame
            A DataFrame with columns ['name', 'cluster', 'cluster label']
            mapping each ingredient to its cluster (the normalized ingredient name).
        """
        model_cut = AgglomerativeClustering(
            distance_threshold=self.cluster_threshold,
            n_clusters=None,
            metric="cosine",
            linkage="average"
        ).fit(embeddings)

        ingredients_df = pd.DataFrame({"name": ingredients, "cluster": model_cut.labels_})
        temp = pd.merge(
            ingredients_df,
            ingredients_count.rename("count"),
            how="left",
            left_on="name",
            right_index=True,
        )

        # étiquette du cluster = ingrédient le plus fréquent
        idx_max = temp.groupby("cluster")["count"].idxmax()
        cluster_labels = temp.loc[idx_max, ["name", "cluster"]].rename(columns={"name": "cluster label"})

        ingredients_df = pd.merge(ingredients_df, cluster_labels, on="cluster")
        return ingredients_df

    def _compute_pca_on_cooccurrence(
        self,
        recipes: pd.DataFrame,
        ingredients_df: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Compute PCA on the ingredient cluster co-occurrence matrix.

        This method builds a matrix of how often ingredient *clusters*
        co-occur within the same recipes. It applies log-transform
        (np.log1p) and then PCA to this matrix.

        Parameters
        ----------
        recipes : pd.DataFrame
            The main recipes DataFrame, used to find co-occurrences.
        ingredients_df : pd.DataFrame
            The clustered ingredients DataFrame from `_cluster_ingredients`.

        Returns
        -------
        Tuple[pd.DataFrame, pd.DataFrame]
            A tuple containing:
            - coords (pd.DataFrame): The PCA coordinates (dimensions) for
              each cluster label.
            - cluster_labels (pd.DataFrame): A DataFrame mapping cluster IDs
              to their string labels.
        """
        # Construction table recette-ingrédient
        ingredients_by_recipe = pd.DataFrame(
            recipes["ingredients"].apply(ast.literal_eval).explode()
        )
        ingredients_by_recipe["id_recipe"] = ingredients_by_recipe.index.to_list()

        ingredients_by_recipe = pd.merge(
            ingredients_by_recipe,
            ingredients_df,
            left_on="ingredients",
            right_on="name",
        )

        cluster_labels = ingredients_df[["cluster", "cluster label"]].drop_duplicates()

        # Construction de la matrice de occcurrence
        cooc = np.zeros((len(cluster_labels), len(cluster_labels)), int)
        index_map = {label: i for i, label in enumerate(cluster_labels["cluster label"])}

        for recipe in range(len(recipes)):
            ings_recipe = ingredients_by_recipe.loc[
                ingredients_by_recipe["id_recipe"] == recipe, "cluster label"
            ]
            for _i, ing_recipe_h in enumerate(ings_recipe):
                for _j, ing_recipe_v in enumerate(ings_recipe):
                    cooc[index_map[ing_recipe_h], index_map[ing_recipe_v]] += 1

        log_cooc = np.log1p(cooc) # Atténue les effets de la distribution exponentielle
        pca = PCA(n_components=self.n_pca_components)
        X_proj = pca.fit_transform(log_cooc)

        dim_names = [f"Dim{i+1}" for i in range(self.n_pca_components)]
        coords = pd.DataFrame(X_proj, columns=dim_names)
        coords["cluster"] = cluster_labels["cluster"].to_numpy()
        coords = pd.merge(coords, cluster_labels, on="cluster", how="left")

        return coords, cluster_labels

    def _add_pca_features(
        self,
        recipes: pd.DataFrame,
        ingredients_df: pd.DataFrame,
        coords: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Add PCA-based cluster coordinates to each recipe as averaged features.

        For each recipe, this method finds the clusters of its ingredients,
        retrieves the PCA coordinates for those clusters (from `coords`),
        and calculates the mean of these coordinates. These mean values
        are added as new 'DimX' columns to the recipes DataFrame.

        Note: Dimensions 'Dim1' and 'Dim3' are excluded as they are
        assumed to relate only to ingredient frequency.

        Parameters
        ----------
        recipes : pd.DataFrame
            The main recipes DataFrame.
        ingredients_df : pd.DataFrame
            The clustered ingredients DataFrame.
        coords : pd.DataFrame
            The PCA coordinates for each cluster.

        Returns
        -------
        pd.DataFrame
            The `recipes` DataFrame updated with new 'DimX' feature columns.
        """
        recipes["ingredients_list"] = recipes["ingredients"].apply(ast.literal_eval)
        ingredient_to_cluster = dict(zip(ingredients_df["name"], ingredients_df["cluster label"]))

        # on exclut les axes Dim1 et Dim3 (uniquement liés à la fréquence des ingrédients)
        dims_to_use = [col for col in coords.columns if col.startswith("Dim") and col not in {"Dim1", "Dim3"}]
        cluster_coords = coords.set_index("cluster label")[dims_to_use]

        def get_recipe_coords(ingredient_list: List[str]) -> pd.Series:
            clusters = [ingredient_to_cluster[i] for i in ingredient_list if i in ingredient_to_cluster]
            if not clusters:
                return pd.Series([np.nan] * len(dims_to_use), index=dims_to_use)
            repeated_coords = cluster_coords.loc[clusters]
            return repeated_coords.mean()

        recipes[dims_to_use] = recipes["ingredients_list"].apply(get_recipe_coords)
        return recipes

    # ======================================================
    # Reporting (stub)
    # ======================================================

    def generate_report(self, result: AnalysisResult, path: str) -> dict[str, str]:
        """
        Stub report generator.

        (This is a placeholder and does not generate a real report).

        Parameters
        ----------
        result : AnalysisResult
            The result object returned by the `analyze` method.
        path : str
            The file path where the report should be saved.

        Returns
        -------
        dict[str, str]
            A dictionary containing paths to the generated report files.
        """
        return {"table_path": str(path), "summary_path": str(path)}