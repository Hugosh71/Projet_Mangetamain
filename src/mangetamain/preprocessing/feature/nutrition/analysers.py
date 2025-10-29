"""Nutrition analyser module."""

from __future__ import annotations
import ast
import pandas as pd
from ...interfaces import Analyser, AnalysisResult


class NutritionAnalyser(Analyser):
    """Analyser computing nutrition-based features from recipe metadata."""

    def analyze(
        self,
        recipes: pd.DataFrame,
        interactions: pd.DataFrame | None = None,
        **kwargs: object,
    ) -> AnalysisResult:
        # Stub fallback when minimal input (no nutrition column)
        if "nutrition" not in recipes.columns or recipes["nutrition"].dropna().empty:
            return AnalysisResult(
                table=pd.DataFrame({"_stub": [True]}),
                summary={},
            )

        nutrition_df = pd.DataFrame(
            recipes["nutrition"].dropna().apply(ast.literal_eval).tolist(),
            columns=["calories", "fat", "sugar", "sodium", "protein", "sat_fat", "carbs"],
        )

        nutrition_df.index = recipes["nutrition"].dropna().index

        base_cols = [c for c in ["id", "name"] if c in recipes.columns]
        df_full = pd.concat([recipes.loc[nutrition_df.index, base_cols], nutrition_df], axis=1)

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

    def generate_report(self, result: AnalysisResult, path):
        """Write nutrition_table.csv and nutrition_summary.csv into the given path."""
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
