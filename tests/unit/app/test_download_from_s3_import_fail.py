from __future__ import annotations

import builtins
from pathlib import Path

from src.app.download_from_s3 import download_from_s3


def test_download_from_s3_import_failure_triggers_stub(
    monkeypatch, tmp_path: Path
) -> None:
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):  # type: ignore[no-redef]
        if name == "boto3":
            raise ImportError("simulated missing boto3")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    out = download_from_s3(dest_dir=tmp_path)
    assert out.exists()
    assert out.name == "recipes_merged.csv.gz"
