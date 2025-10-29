"""Ingredients analyser module."""

from __future__ import annotations

import ast

import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA

from ...interfaces import Analyser, AnalysisResult


class IngredientsAnalyser(Analyser):
    """Analyser that extracts semantic and PCA-based features from recipe ingredients."""

    DEFAULT_CLUSTER_THRESHOLD: float = 0.5
    DEFAULT_N_PCA_COMPONENTS: int = 10
    DEFAULT_MODEL_NAME: str = "all-mpnet-base-v2"

    AXES_PHRASES: dict[str, tuple[str, str]] = {
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
        """Initialize the IngredientsAnalyser."""
        self.cluster_threshold = cluster_threshold or self.DEFAULT_CLUSTER_THRESHOLD
        self.n_pca_components = n_pca_components or self.DEFAULT_N_PCA_COMPONENTS
        self.embedding_model_name = embedding_model or self.DEFAULT_MODEL_NAME
        # Lazy-load the embedding model only when needed to keep tests lightweight
        self.model: object | None = None

    # ======================================================
    # Main public method
    # ======================================================

    def analyze(
        self,
        recipes: pd.DataFrame,
        interactions: pd.DataFrame,
        **kwargs: object,
    ) -> AnalysisResult:
        """Main analysis pipeline producing semantic and PCA-based features."""
        # Stub fallback when minimal input (no ingredients column)
        if (
            "ingredients" not in recipes.columns
            or recipes["ingredients"].dropna().empty
        ):
            return AnalysisResult(
                table=pd.DataFrame({"_stub": [True]}),
                summary={},
            )

        ingredients, ingredients_count = self._extract_ingredients(recipes)
        embeddings = self._compute_embeddings(ingredients)
        scores_df = self._compute_semantic_scores(ingredients, embeddings)

        recipes = self._add_semantic_features(recipes, scores_df)

        ingredients_df = self._cluster_ingredients(
            ingredients, embeddings, ingredients_count
        )
        coords, cluster_labels = self._compute_pca_on_cooccurrence(
            recipes, ingredients_df
        )

        recipes = self._add_pca_features(recipes, ingredients_df, coords)

        # Ne renvoyer que l'identifiant et les nouvelles features
        feature_cols = [
            col
            for col in recipes.columns
            if col.startswith("score_") or col.startswith("Dim")
        ]
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

    def _extract_ingredients(
        self, recipes: pd.DataFrame
    ) -> tuple[list[str], pd.Series]:
        """Extract unique ingredients and their frequencies from the recipes DataFrame."""
        ingredients_series = recipes["ingredients"].apply(ast.literal_eval).explode()
        ingredients_count = ingredients_series.value_counts()
        ingredients = pd.unique(ingredients_series).tolist()
        return ingredients, ingredients_count

    def _compute_embeddings(self, ingredients: list[str]) -> np.ndarray:
        """Compute embeddings for all ingredients using a sentence transformer."""
        model = self._get_model()
        return model.encode(ingredients)

    def _get_model(self):  # returns a SentenceTransformer instance
        if self.model is None:
            try:
                from sentence_transformers import SentenceTransformer  # type: ignore
            except ImportError as e:  # pragma: no cover - explicit error path
                raise ImportError(
                    "sentence-transformers is required for IngredientsAnalyser. "
                    "Install with `poetry install --with ml` or `pip install sentence-transformers`."
                ) from e
            self.model = SentenceTransformer(self.embedding_model_name)
        return self.model

    def _compute_semantic_scores(
        self, ingredients: list[str], embeddings: np.ndarray
    ) -> pd.DataFrame:
        """Compute cosine similarity scores between ingredients and semantic axes."""
        model = self._get_model()
        axis_vecs = {
            name: model.encode(pos) - model.encode(neg)
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
        self, recipes: pd.DataFrame, scores_df: pd.DataFrame
    ) -> pd.DataFrame:
        """Add semantic scores to the recipes DataFrame."""
        for axis in scores_df.columns:
            score_map = scores_df[axis].to_dict()
            recipes[f"score_{axis}"] = recipes["ingredients"].apply(
                lambda ingr_list, score_map=score_map: np.mean(
                    [
                        score_map[i]
                        for i in ast.literal_eval(ingr_list)
                        if i in score_map
                    ]
                )
            )
        return recipes

    def _cluster_ingredients(
        self,
        ingredients: list[str],
        embeddings: np.ndarray,
        ingredients_count: pd.Series,
    ) -> pd.DataFrame:
        """Cluster ingredients based on embeddings using hierarchical clustering."""
        model_cut = AgglomerativeClustering(
            distance_threshold=self.cluster_threshold,
            n_clusters=None,
            metric="cosine",
            linkage="average",
        ).fit(embeddings)

        ingredients_df = pd.DataFrame(
            {"name": ingredients, "cluster": model_cut.labels_}
        )
        temp = pd.merge(
            ingredients_df,
            ingredients_count.rename("count"),
            how="left",
            left_on="name",
            right_index=True,
        )

        # étiquette du cluster = ingrédient le plus fréquent
        idx_max = temp.groupby("cluster")["count"].idxmax()
        cluster_labels = temp.loc[idx_max, ["name", "cluster"]].rename(
            columns={"name": "cluster label"}
        )

        ingredients_df = pd.merge(ingredients_df, cluster_labels, on="cluster")
        return ingredients_df

    def _compute_pca_on_cooccurrence(
        self, recipes: pd.DataFrame, ingredients_df: pd.DataFrame
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Compute PCA on the ingredient co-occurrence matrix."""
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
        index_map = {
            label: i for i, label in enumerate(cluster_labels["cluster label"])
        }

        for recipe in range(len(recipes)):
            ings_recipe = ingredients_by_recipe.loc[
                ingredients_by_recipe["id_recipe"] == recipe, "cluster label"
            ]
            for _i, ing_recipe_h in enumerate(ings_recipe):
                for _j, ing_recipe_v in enumerate(ings_recipe):
                    cooc[index_map[ing_recipe_h], index_map[ing_recipe_v]] += 1

        log_cooc = np.log1p(cooc)  # Atténue les effets de la distribution exponentielle
        pca = PCA(n_components=self.n_pca_components)
        X_proj = pca.fit_transform(log_cooc)

        dim_names = [f"Dim{i+1}" for i in range(self.n_pca_components)]
        coords = pd.DataFrame(X_proj, columns=dim_names)
        coords["cluster"] = cluster_labels["cluster"].to_numpy()
        coords = pd.merge(coords, cluster_labels, on="cluster", how="left")

        return coords, cluster_labels

    def _add_pca_features(
        self, recipes: pd.DataFrame, ingredients_df: pd.DataFrame, coords: pd.DataFrame
    ) -> pd.DataFrame:
        """Add PCA-based cluster coordinates to each recipe as averaged features."""
        recipes["ingredients_list"] = recipes["ingredients"].apply(ast.literal_eval)
        ingredient_to_cluster = dict(
            zip(ingredients_df["name"], ingredients_df["cluster label"], strict=False)
        )

        # on exclut les axes Dim1 et Dim3 (uniquement liés à la fréquence des ingrédients)
        dims_to_use = [
            col
            for col in coords.columns
            if col.startswith("Dim") and col not in {"Dim1", "Dim3"}
        ]
        cluster_coords = coords.set_index("cluster label")[dims_to_use]

        def get_recipe_coords(ingredient_list: list[str]) -> pd.Series:
            clusters = [
                ingredient_to_cluster[i]
                for i in ingredient_list
                if i in ingredient_to_cluster
            ]
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
        """Write ingredients_table.csv and ingredients_summary.csv into the given path."""
        from pathlib import Path

        import pandas as pd

        p = Path(path)
        if p.is_dir():
            out_table = p / "ingredients_table.csv"
            out_summary = p / "ingredients_summary.csv"
        else:
            out_table = p.parent / "ingredients_table.csv"
            out_summary = p.parent / "ingredients_summary.csv"

        out_table.parent.mkdir(parents=True, exist_ok=True)

        result.table.to_csv(out_table, index=False)
        summary_df = pd.DataFrame([result.summary]).melt(
            var_name="metric", value_name="value"
        )
        summary_df.to_csv(out_summary, index=False)

        return {"table_path": str(out_table), "summary_path": str(out_summary)}
