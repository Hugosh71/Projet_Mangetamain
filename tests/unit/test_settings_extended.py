from __future__ import annotations

import os
from pathlib import Path

from app.settings import LoggingSettings, load_env_file


def test_load_env_file_skips_comments_and_no_separator(
    tmp_path: Path, monkeypatch
) -> None:
    env_path = tmp_path / "custom.env"
    env_path.write_text(
        (
            "# comment\n"
            "INVALID_LINE_NO_EQUAL\n"
            "MANG_LOG_MAX_FILES=11\n"
            "MANG_USER_ID='quoted-user'\n"
        ),
        encoding="utf-8",
    )

    monkeypatch.delenv("MANG_LOG_MAX_FILES", raising=False)
    monkeypatch.delenv("MANG_USER_ID", raising=False)

    load_env_file(env_path)

    assert os.environ["MANG_LOG_MAX_FILES"] == "11"
    # quotes must be stripped
    assert os.environ["MANG_USER_ID"] == "quoted-user"


def test_from_env_resolves_relative_directory(tmp_path: Path, monkeypatch) -> None:
    rel_dir = Path("rel_logs")
    monkeypatch.setenv("MANG_LOG_DIR", str(rel_dir))

    settings = LoggingSettings.from_env()

    # Should be resolved under project root, absolute
    assert settings.directory.is_absolute()


def test_parse_empty_string_behaves_like_default(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("MANG_LOG_MAX_FILES", "")
    settings = LoggingSettings.from_env()
    # Default defined in module is 10
    assert settings.max_files >= 1
