"""Steps analysers (stubs)."""

from __future__ import annotations

import pandas as pd

from ..interfaces import Analyser, AnalysisResult


class StepsAnalyser(Analyser):
    def analyze(
        self,
        recipes: pd.DataFrame,
        interactions: pd.DataFrame,
        **kwargs: object,
    ) -> AnalysisResult:
        return AnalysisResult(table=recipes.assign(_stub=True), summary={})

    def generate_report(self, result: AnalysisResult, path):
        return {"table_path": str(path), "summary_path": str(path)}


