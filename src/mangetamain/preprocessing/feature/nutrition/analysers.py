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
        if "nutrition" not in recipes.columns or recipes["nutrition"].dropna().empty:
            return AnalysisResult(
                table=pd.DataFrame({"_stub": [True]}),
                summary={},
            )

        nutrition_series = recipes["nutrition"].dropna()
        nutrition_df = pd.DataFrame(
            nutrition_series.apply(ast.literal_eval).tolist(),
            columns=[
                "calories",
                "fat",
                "sugar",
                "sodium",
                "protein",
                "sat_fat",
                "carbs",
            ],
            index=nutrition_series.index,
        )

        # Ensure id and name are present and aligned
        if "id" in recipes.columns:
            id_series = recipes.loc[nutrition_df.index, "id"].rename("id")
        else:
            id_series = pd.Series(
                range(len(nutrition_df)), index=nutrition_df.index, name="id"
            )

        if "name" in recipes.columns:
            name_series = recipes.loc[nutrition_df.index, "name"].rename("name")
        else:
            name_series = pd.Series(
                [None] * len(nutrition_df), index=nutrition_df.index, name="name"
            )

        df_full = pd.concat([id_series, name_series, nutrition_df], axis=1)

        # feature 1 : energy density
        df_full["energy_density"] = df_full["calories"] / (
            df_full["carbs"] + df_full["protein"] + df_full["fat"] + 1
        )

        # feature 2 : protein ratio
        df_full["protein_ratio"] = df_full["protein"] / (df_full["calories"] + 1)

        # feature 3 : fat ratio
        df_full["fat_ratio"] = df_full["fat"] / (df_full["calories"] + 1)

        # feature 4 : nutrient balance index
        df_full["nutrient_balance_index"] = (
            df_full["protein"]
            - (df_full["fat"] + df_full["sugar"] + df_full["sodium"]) / 3
        ) / (df_full["calories"] + 1)

        df_export = df_full[
            [
                "id",
                "name",
                "energy_density",
                "protein_ratio",
                "fat_ratio",
                "nutrient_balance_index",
            ]
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
        from pathlib import Path

        path = Path(path)
        if path.is_dir():
            out_table = path / "nutrition_table.csv"
            out_summary = path / "nutrition_summary.csv"
        else:
            out_table = path.parent / "nutrition_table.csv"
            out_summary = path.parent / "nutrition_summary.csv"

        out_table.parent.mkdir(parents=True, exist_ok=True)

        # Write table
        # Keep a simple CSV (no custom separator) for consistency with other analyzers
        result.table.to_csv(out_table, index=False)

        # Write summary as key,value rows
        summary_df = pd.DataFrame([result.summary]).melt(
            var_name="metric", value_name="value"
        )
        summary_df.to_csv(out_summary, index=False)

        return {"table_path": str(out_table), "summary_path": str(out_summary)}


# Partie test
# if __name__ == "__main__":
#     import pandas as pd

#     path = "C:/Users/fanch/OneDrive/Bureau/mangetamain/data/RAW_recipes.csv"

#     recipes_df = pd.read_csv(path)
#     interactions_df = pd.DataFrame()

#     # analyse
#     analyser = NutritionAnalyser()
#     result = analyser.analyze(recipes_df, interactions_df)

#     print(result.table.head())
#     print("\nRésumé :")
#     print(result.summary)
