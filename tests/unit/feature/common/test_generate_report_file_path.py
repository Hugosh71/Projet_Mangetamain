from __future__ import annotations

from pathlib import Path

import pandas as pd

from mangetamain.preprocessing.feature.seasonality.analyzers import SeasonalityAnalyzer
from mangetamain.preprocessing.feature.steps.analysers import StepsAnalyser
from mangetamain.preprocessing.feature.ingredients.analysers import IngredientsAnalyser
from mangetamain.preprocessing.feature.nutrition.analysers import NutritionAnalyser
from mangetamain.preprocessing.interfaces import AnalysisResult


def test_generate_report_with_file_path_else_branch(tmp_path: Path) -> None:
    dummy_file = tmp_path / "placeholder.txt"

    result = AnalysisResult(table=pd.DataFrame([{"_stub": True}]), summary={})

    out_s = SeasonalityAnalyzer().generate_report(result, dummy_file)
    assert Path(out_s["table_path"]).parent == tmp_path

    out_st = StepsAnalyser().generate_report(result, dummy_file)
    assert Path(out_st["table_path"]).parent == tmp_path

    out_i = IngredientsAnalyser().generate_report(result, dummy_file)
    assert Path(out_i["table_path"]).parent == tmp_path

    out_n = NutritionAnalyser().generate_report(result, dummy_file)
    assert Path(out_n["table_path"]).parent == tmp_path


