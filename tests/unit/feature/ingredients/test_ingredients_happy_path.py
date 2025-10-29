from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from mangetamain.preprocessing.feature.ingredients.analysers import (
    IngredientsAnalyser,
)


class _FakeModel:
    def encode(self, x: Any):
        def vec(s: str) -> np.ndarray:
            # Deterministic tiny embedding from string
            a = sum(ord(c) for c in s) % 7
            b = (sum(ord(c) * 3 for c in s) % 11)
            c = (len(s) * 5) % 13
            return np.array([float(a), float(b), float(c)], dtype=float)

        if isinstance(x, (list, tuple)):
            return np.vstack([vec(str(s)) for s in x])
        return vec(str(x))


def test_ingredients_analyse_and_report_with_mocked_model(tmp_path: Path, monkeypatch) -> None:
    recipes = pd.DataFrame([
        {"id": 1, "name": "A", "ingredients": "['salt','water']"},
        {"id": 2, "name": "B", "ingredients": "['flour','water']"},
        {"id": 3, "name": "C", "ingredients": "['salt','flour']"},
    ])
    interactions = pd.DataFrame()

    analyser = IngredientsAnalyser(n_pca_components=2)

    # Patch the internal model getter to avoid network/model load
    monkeypatch.setattr(analyser, "_get_model", lambda: _FakeModel())

    # Ensure we have at least 3 clusters regardless of distance threshold
    def fake_cluster(ingredients, embeddings, ingredients_count):  # type: ignore
        import pandas as pd
        clusters = [i % 3 for i in range(len(ingredients))]
        df = pd.DataFrame({"name": ingredients, "cluster": clusters})
        labels = (
            pd.DataFrame({"cluster": [0, 1, 2], "cluster label": ["C0", "C1", "C2"]})
        )
        return pd.merge(df, labels, on="cluster")

    monkeypatch.setattr(analyser, "_cluster_ingredients", fake_cluster)

    result = analyser.analyze(recipes, interactions)

    # Semantic score columns must exist
    assert any(col.startswith("score_") for col in result.table.columns)

    # PCA-based feature columns (Dim2 only, since Dim1 excluded)
    dims = [c for c in result.table.columns if c.startswith("Dim")]
    assert "Dim2" in dims

    out = analyser.generate_report(result, tmp_path)
    assert Path(out["table_path"]).name == "ingredients_table.csv"
    assert Path(out["summary_path"]).name == "ingredients_summary.csv"
    assert Path(out["table_path"]).exists()
    assert Path(out["summary_path"]).exists()


