"""Steps analysers (stubs)."""

from __future__ import annotations

import pandas as pd

from ...interfaces import Analyser, AnalysisResult


class StepsAnalyser(Analyser):
    def analyze(
        self,
        recipes: pd.DataFrame,
        interactions: pd.DataFrame,
        **kwargs: object,
    ) -> AnalysisResult:
        # On calcule des stats de base
        summary = {
            "moyenne_etapes": recipes["n_steps"].mean(),
            "moyenne_ingredients": recipes["n_ingredients"].mean(),
            "correlation_steps_ingredients": recipes["n_steps"].corr(recipes["n_ingredients"]),
            "nb_clusters": recipes["cluster_label_ing_steps"].nunique()
        }

        # On ajoute éventuellement une colonne utile
        table = recipes.copy()
        table["_has_steps"] = table["n_steps"] > 0

        return AnalysisResult(table=table, summary=summary)

    def generate_report(self, result: AnalysisResult, path: str):
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)

        # Sauvegarde du graphique
        plt.figure(figsize=(8, 6))
        for label in result.table["cluster_label_ing_steps"].unique():
            subset = result.table[result.table["cluster_label_ing_steps"] == label]
            plt.scatter(
                subset["n_steps"],
                subset["n_ingredients"],
                label=f"Cluster {label}",
                alpha=0.6
            )

        plt.xlabel("Nombre d'étapes")
        plt.ylabel("Nombre d'ingrédients")
        plt.title("Recettes par features d'étapes et d'ingrédients")
        plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")

        fig_path = path / "steps_clusters.png"
        plt.tight_layout()
        plt.savefig(fig_path)
        plt.close()

        # Sauvegarde du résumé en CSV ou JSON
        summary_path = path / "steps_summary.csv"
        pd.DataFrame([result.summary]).to_csv(summary_path, index=False)

        return {
            "table_path": str(fig_path),
            "summary_path": str(summary_path)
        }