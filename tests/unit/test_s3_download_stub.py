from __future__ import annotations

from pathlib import Path

from app.download_from_s3 import download_from_s3_stub


def test_download_from_s3_stub_creates_file(tmp_path: Path) -> None:
    dest = tmp_path / "clustering"
    local = download_from_s3_stub(dest_dir=dest)
    assert local.exists()
