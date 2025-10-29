"""Nutrition analyser module.

This module defines the NutritionAnalyser`class, which extracts and computes
nutritional-based features from recipe metadata (calories, fat, sugar, protein, etc.).
It follows the `Analyser` interface and produces an `AnalysisResult` object
containing a feature table and summary statistics.
"""

from __future__ import annotations
import ast
import pandas as pd
from ...interfaces import Analyser, AnalysisResult


class NutritionAnalyser(Analyser):
    """
    Analyser computing nutrition-based features from recipe metadata.

    This analyser extracts structured nutritional data (e.g., calories, fat,
    protein, sugar) from the "nutrition" field of the recipes DataFrame.
    It computes several derived indicators useful for downstream modeling
    or recommendation tasks, such as energy density and nutrient balance.

    Attributes
    ----------
    None explicitly defined — this class is stateless.
    """

    # pipeline

    def analyze(
        self,
        recipes: pd.DataFrame,
        interactions: pd.DataFrame | None = None,
        **kwargs: object,
    ) -> AnalysisResult:
        """
        Compute nutrition-based features for each recipe.

        This method parses the "nutrition" field of the recipes DataFrame,
        extracts individual nutrient values, and derives higher-level
        indicators summarizing the nutritional composition of each recipe.

        The computed features include:
        - **energy_density**: ratio of calories to total macronutrients (fat + carbs + protein).
        - **protein_ratio**: fraction of calories contributed by proteins.
        - **fat_ratio**: fraction of calories contributed by fats.
        - **nutrient_balance_index**: heuristic index combining protein and negative nutrients
          (fat, sugar, sodium) normalized by total calories.

        Parameters
        ----------
        recipes : pd.DataFrame
            DataFrame containing recipe metadata.
            Must include a "nutrition" column, typically a stringified list such as:
            "[calories, fat, sugar, sodium, protein, sat_fat, carbs]".
        interactions : pd.DataFrame, optional
            DataFrame of user interactions (unused in this analyser, kept for interface compatibility).
        **kwargs : object
            Additional arguments passed for interface consistency (ignored).

        Returns
        -------
        AnalysisResult
            Object containing:
            - **table**: a DataFrame with one row per recipe and the computed nutrition features.
            - **summary**: a dictionary of global mean values and recipe count.

        Raises
        ------
        ValueError
            If the "nutrition" column is missing from the recipes DataFrame.
        """
        # safety check
        if "nutrition" not in recipes.columns:
            raise ValueError("Column 'nutrition' is missing in recipes DataFrame.")

        nutrition_df = pd.DataFrame(
            recipes["nutrition"].dropna().apply(ast.literal_eval).tolist(),
            columns=["calories", "fat", "sugar", "sodium", "protein", "sat_fat", "carbs"],
        )
        nutrition_df.index = recipes["nutrition"].dropna().index

        base_cols = [c for c in ["id", "name"] if c in recipes.columns]
        df_full = pd.concat([recipes.loc[nutrition_df.index, base_cols], nutrition_df], axis=1)

        # features
        df_full["energy_density"] = df_full["calories"] / (
            df_full["carbs"] + df_full["protein"] + df_full["fat"] + 1
        )
        df_full["protein_ratio"] = df_full["protein"] / (df_full["calories"] + 1)
        df_full["fat_ratio"] = df_full["fat"] / (df_full["calories"] + 1)
        df_full["nutrient_balance_index"] = (
            (df_full["protein"] - (df_full["fat"] + df_full["sugar"] + df_full["sodium"]) / 3)
            / (df_full["calories"] + 1)
        )

        df_export = df_full[
            base_cols + ["energy_density", "protein_ratio", "fat_ratio", "nutrient_balance_index"]
        ]

        # summary
        summary = {
            "mean_energy_density": float(df_export["energy_density"].mean()),
            "mean_protein_ratio": float(df_export["protein_ratio"].mean()),
            "mean_fat_ratio": float(df_export["fat_ratio"].mean()),
            "mean_balance_index": float(df_export["nutrient_balance_index"].mean()),
            "n_recipes": len(df_export),
        }

        return AnalysisResult(table=df_export, summary=summary)

    # generating csv

    def generate_report(self, result: AnalysisResult, path):
        """
        Generate and save the nutrition feature outputs (stub implementation).

        Saves the computed feature table to a CSV file in the given directory,
        and returns the file paths and summary information.

        Parameters
        ----------
        result : AnalysisResult
            The result object returned by the `analyze` method, containing
            a DataFrame (`result.table`) and a summary dictionary.
        path : Path or str
            Destination folder path where the output CSV will be written.

        Returns
        -------
        dict[str, object]
            Dictionary containing:
            - `"table_path"`: path to the saved CSV file.
            - `"summary"`: the summary statistics dictionary.
        """
        result.table.to_csv(path / "features_nutrition.csv", index=False, sep=";")
        return {
            "table_path": str(path / "features_nutrition.csv"),
            "summary": result.summary,
        }


#test
# if __name__ == "__main__":
#     import pandas as pd
#     path = "C:/Users/fanch/OneDrive/Bureau/mangetamain/data/RAW_recipes.csv"
#     recipes_df = pd.read_csv(path)
#     interactions_df = pd.DataFrame()
#     analyser = NutritionAnalyser()
#     result = analyser.analyze(recipes_df, interactions_df)
#     print(result.table.head())
#     print("\nRésumé :")
#     print(result.summary)
