from __future__ import annotations

from pathlib import Path
import types

from src.app.download_from_s3 import download_from_s3, download_from_s3_stub


def test_download_from_s3_stub_existing_file(tmp_path: Path) -> None:
    # First touch the file via stub
    first = download_from_s3_stub(key="already.csv", dest_dir=tmp_path)
    assert first.exists()
    # Second call should hit the "already local" branch
    second = download_from_s3_stub(key="already.csv", dest_dir=tmp_path)
    assert second.exists()


class _SuccessfulBoto3(types.ModuleType):
    class session:  # type: ignore
        class Session:  # type: ignore
            def client(self, *_args, **_kwargs):  # type: ignore
                class _Client:
                    def download_file(self, _bucket, _key, local_path):  # type: ignore
                        Path(local_path).parent.mkdir(parents=True, exist_ok=True)
                        Path(local_path).write_text("ok")

                return _Client()


def test_download_from_s3_successful_path(monkeypatch, tmp_path: Path) -> None:
    # Inject a fake boto3 that succeeds
    monkeypatch.setitem(__import__("sys").modules, "boto3", _SuccessfulBoto3("boto3"))
    out = download_from_s3(dest_dir=tmp_path, key="file.csv")
    assert out.exists()
    assert out.read_text() == "ok"


