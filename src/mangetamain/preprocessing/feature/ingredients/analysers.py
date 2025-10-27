"""Ingredients analysers (stubs)."""

from __future__ import annotations
import ast

import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from ...interfaces import Analyser, AnalysisResult


class IngredientsAnalyser(Analyser):
    def analyze(
        self,
        recipes: pd.DataFrame,
        interactions: pd.DataFrame,
        **kwargs: object,
    ) -> AnalysisResult:
        
        ingredients = recipes['ingredients'].apply(ast.literal_eval).explode()
        ingredients = pd.unique(ingredients).tolist()
        model = SentenceTransformer("all-mpnet-base-v2")
        embeddings = model.encode(ingredients)

        axes_phrases = {
        "sweet_savory": ("sweet dessert flavor", "savory meal flavor"),
        "spicy_mild": ("spicy hot food", "mild gentle flavor"),
        "lowcal_rich": ("low-calorie healthy food", "rich and fatty dish"),
        "vegetarian_meat": ("vegetarian food without meat", "meat-based dish"),
        "solid_liquid": ("solid food", "liquid food or drink"),
        "raw_processed": ("raw natural ingredient", "processed or prepared food"),
        "western_exotic": ("typical western food", "exotic or asian food"),
        }

        def axis_vector(model, pos_name, neg_name):
            return model.encode(pos_name) - model.encode(neg_name)

        axis_vecs = {axe_name: axis_vector(model, pos_name, neg_name) 
                    for axe_name, (pos_name, neg_name) in axes_phrases.items()}

        axes_names = list(axis_vecs.keys())
        axis_matrix = np.stack(list(axis_vecs.values()))  # shape (n_axes, dim embeddings)

        # Normaliser embeddings et axes (pour cosinus)
        emb_norm = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        axis_norm = axis_matrix / np.linalg.norm(axis_matrix, axis=1, keepdims=True)

        # Produit matriciel pour cosinus
        # result[i, j] = cosine(ingredient i, axis j)
        cos_sim_matrix = np.dot(emb_norm, axis_norm.T)   # shape (n_ingredients, n_axes)

        scores_df = pd.DataFrame(cos_sim_matrix, index=ingredients, columns=axes_names)

        return AnalysisResult(table=recipes.assign(_stub=True), summary={})

    def generate_report(self, result: AnalysisResult, path):
        return {"table_path": str(path), "summary_path": str(path)}
