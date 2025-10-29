from __future__ import annotations

import types
from pathlib import Path

import pytest

from src.app.download_from_s3 import download_from_s3


class _FailingBoto3(types.ModuleType):
    class session:  # type: ignore
        class Session:  # type: ignore
            def client(self, *_args, **_kwargs):  # type: ignore
                class _Client:
                    def download_file(self, *_a, **_k):  # type: ignore
                        raise RuntimeError("simulated network failure")

                return _Client()


def test_download_from_s3_falls_back_to_stub(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    # Inject a fake boto3 that raises on download to force stub path
    monkeypatch.setitem(__import__("sys").modules, "boto3", _FailingBoto3("boto3"))

    out = download_from_s3(
        bucket="mangetamain", key="recipes_merged.csv.gz", dest_dir=tmp_path
    )
    assert out.exists()
    assert out.name == "recipes_merged.csv.gz"
