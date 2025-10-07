"""Unit tests for the logging configuration and settings modules."""

from __future__ import annotations

import logging
import os
from pathlib import Path

import pytest

from mangetamain.logging_config import configure_logging, get_logger, reset_logging
from mangetamain.settings import (
    DEFAULT_LOG_DIR,
    DEFAULT_MAX_LOG_FILES,
    LoggingSettings,
    load_env_file,
)


ENV_KEYS = ("MANG_LOG_DIR", "MANG_LOG_MAX_FILES", "MANG_USER_ID", "MANG_SESSION_ID")


@pytest.fixture(autouse=True)
def _clean_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    saved = {key: os.environ.get(key) for key in ENV_KEYS}
    try:
        yield
    finally:
        for key in ENV_KEYS:
            monkeypatch.delenv(key, raising=False)
        for key, value in saved.items():
            if value is not None:
                os.environ[key] = value


@pytest.fixture(autouse=True)
def _reset_logging() -> None:
    """Ensure each test starts from a fresh logging configuration."""

    reset_logging()
    yield
    reset_logging()


@pytest.fixture
def temp_workdir(tmp_path: Path) -> Path:
    """Switch to a temporary working directory for the duration of a test."""

    origin = Path.cwd()
    os.chdir(tmp_path)
    try:
        yield tmp_path
    finally:
        os.chdir(origin)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_basic_logging_creates_files(temp_workdir: Path) -> None:
    config = configure_logging(log_directory=temp_workdir)

    logger = get_logger("basic")
    logger.debug("debug message")
    logger.error("error message")

    assert config.debug_log_path.exists()
    assert config.error_log_path.exists()

    debug_content = _read(config.debug_log_path)
    error_content = _read(config.error_log_path)

    assert "debug message" in debug_content
    assert "error message" in error_content


def test_error_file_contains_only_error_records(temp_workdir: Path) -> None:
    config = configure_logging(log_directory=temp_workdir)

    logger = get_logger("levels")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")

    assert "error message" in _read(config.error_log_path)
    assert "info message" not in _read(config.error_log_path)
    assert "warning message" not in _read(config.error_log_path)


@pytest.mark.parametrize("requested", [None, 1, 3, 5])
def test_rotation_prunes_old_files(requested: int | None, temp_workdir: Path) -> None:
    configure_logging(log_directory=temp_workdir, max_log_files=requested)

    for index in range(6):
        configure_logging(
            log_directory=temp_workdir,
            max_log_files=requested,
            reset_existing=True,
        )

    keep = requested or 10
    debug_files = sorted(temp_workdir.glob("debug-*.log"))
    error_files = sorted(temp_workdir.glob("error-*.log"))

    assert len(debug_files) <= keep
    assert len(error_files) <= keep


def test_configure_logging_returns_cached_configuration(temp_workdir: Path) -> None:
    first = configure_logging(log_directory=temp_workdir)
    second = configure_logging()

    assert first is second


def test_contextual_information_is_present(temp_workdir: Path) -> None:
    config = configure_logging(log_directory=temp_workdir)
    logger = get_logger("context")

    logger.info("context message")

    content = _read(config.debug_log_path)

    assert f"run={config.run_identifier}" in content
    assert "user=" in content
    assert "session=" in content


def test_reset_logging_removes_handlers(temp_workdir: Path) -> None:
    configure_logging(log_directory=temp_workdir)
    logger = logging.getLogger("mangetamain")

    assert logger.handlers

    reset_logging()

    assert not logger.handlers


def test_logging_settings_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in ENV_KEYS:
        monkeypatch.delenv(key, raising=False)

    settings = LoggingSettings.from_env()

    assert settings.directory == DEFAULT_LOG_DIR
    assert settings.max_files == DEFAULT_MAX_LOG_FILES
    assert settings.user_id is None
    assert settings.session_id is None


def test_logging_settings_respects_environment(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    custom_dir = tmp_path / "custom-logs"
    monkeypatch.setenv("MANG_LOG_DIR", str(custom_dir))
    monkeypatch.setenv("MANG_LOG_MAX_FILES", "7")
    monkeypatch.setenv("MANG_USER_ID", "tester")
    monkeypatch.setenv("MANG_SESSION_ID", "session-xyz")

    settings = LoggingSettings.from_env()

    assert settings.directory == custom_dir.resolve()
    assert settings.max_files == 7
    assert settings.user_id == "tester"
    assert settings.session_id == "session-xyz"


def test_logging_settings_invalid_max_files_uses_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MANG_LOG_MAX_FILES", "not-a-number")

    settings = LoggingSettings.from_env()

    assert settings.max_files == DEFAULT_MAX_LOG_FILES


def test_load_env_file_reads_values(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    env_path = tmp_path / "settings.env"
    env_path.write_text("MANG_LOG_MAX_FILES=12\nMANG_USER_ID=from_env\n", encoding="utf-8")

    monkeypatch.delenv("MANG_LOG_MAX_FILES", raising=False)
    monkeypatch.delenv("MANG_USER_ID", raising=False)

    load_env_file(env_path)

    assert os.environ["MANG_LOG_MAX_FILES"] == "12"
    assert os.environ["MANG_USER_ID"] == "from_env"


def test_load_env_file_respects_override_flag(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    env_path = tmp_path / "settings.env"
    env_path.write_text("MANG_LOG_MAX_FILES=5\n", encoding="utf-8")

    monkeypatch.setenv("MANG_LOG_MAX_FILES", "20")

    load_env_file(env_path)
    assert os.environ["MANG_LOG_MAX_FILES"] == "20"

    load_env_file(env_path, override=True)
    assert os.environ["MANG_LOG_MAX_FILES"] == "5"

