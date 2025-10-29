import logging
from pathlib import Path

import pandas as pd
import pytest

from src.mangetamain.preprocessing.feature.steps.analysers import StepsAnalyser


class TestStepsAnalyser:
    """Pytest class around StepsAnalyser behavior."""

    def _base_recipes(self):
        return pd.DataFrame({
            'minutes': [10, 20, 30, 40, 50],
            'n_steps': [3, 5, 7, 2, 6],
            'n_ingredients': [4, 6, 8, 3, 7],
            'id': [1, 2, 3, 4, 5]
        })

    def test_analyze_and_generate_report(self, tmp_path):
        recipes = self._base_recipes()
        interactions = pd.DataFrame()

        analyser = StepsAnalyser(logger=logging.getLogger("test"))
        result = analyser.analyze(recipes, interactions)

        # Basic structure assertions
        expected_cols = [
            'id', 'minutes', 'n_steps', 'n_ingredients',
            'minutes_z', 'n_steps_z', 'n_ingredients_z',
            'minutes_log', 'cluster_ing_steps', 'cluster_label_ing_steps',
        ]
        for c in expected_cols:
            assert c in result.table.columns

        expected_summary_keys = [
            'moyenne_etapes', 'moyenne_ingredients',
            'correlation_steps_ingredients', 'nb_clusters',
        ]
        for k in expected_summary_keys:
            assert k in result.summary

        out = analyser.generate_report(result, tmp_path)
        table_path = Path(out['table_path'])
        summary_path = Path(out['summary_path'])

        assert table_path.exists(), f"Table CSV not created: {table_path}"
        assert summary_path.exists(), f"Summary CSV not created: {summary_path}"

        df = pd.read_csv(table_path)
        assert 'cluster_label_ing_steps' in df.columns

    def test_missing_required_column_raises(self):
        # remove 'minutes' column to provoke the error
        recipes = self._base_recipes().drop(columns=['minutes'])
        interactions = pd.DataFrame()

        analyser = StepsAnalyser(logger=logging.getLogger("test"))
        with pytest.raises(ValueError):
            analyser.analyze(recipes, interactions)
