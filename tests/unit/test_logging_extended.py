from __future__ import annotations

from pathlib import Path

import pytest
from app.logging_config import (
    _prune_retained_logs,  # type: ignore
    configure_logging,
    get_logger,
    reset_logging,
)


@pytest.fixture(autouse=True)
def _reset_logging_each() -> None:
    reset_logging()
    yield
    reset_logging()


def test_get_logger_without_name_uses_base_logger(tmp_path: Path) -> None:
    configure_logging(log_directory=tmp_path)
    logger = get_logger()
    logger.debug("base logger message")
    # Verify that a message is written into the debug log
    debug_path = next(tmp_path.glob("debug-*.log"))
    text = debug_path.read_text(
        encoding="utf-8"
    )
    assert "base logger message" in text


def test_configure_logging_reads_user_and_session_from_env(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("MANG_LOG_DIR", str(tmp_path))
    monkeypatch.setenv("MANG_USER_ID", "userx")
    monkeypatch.setenv("MANG_SESSION_ID", "sessx")

    config = configure_logging(
        log_directory=None,
        user_id=None,
        session_id=None,
    )
    logger = get_logger("env")
    logger.info("env-driven message")

    content = Path(config.debug_log_path).read_text(
        encoding="utf-8"
    )
    assert "user=userx" in content
    assert "session=sessx" in content


def test_configure_logging_accepts_str_directory_and_prunes_min_keep(
    tmp_path: Path,
) -> None:
    # Use string path to exercise Path conversion branch
    base = tmp_path / "logs"
    base.mkdir()

    # keep computed via max(1, 0)
    for _ in range(3):
        configure_logging(
            log_directory=str(base), max_log_files=0, reset_existing=True
        )

    debug_files = sorted(base.glob("debug-*.log"))
    error_files = sorted(base.glob("error-*.log"))
    assert len(debug_files) <= 1
    assert len(error_files) <= 1


def test_prune_retained_logs_no_files_is_noop(tmp_path: Path) -> None:
    # Call internal helper directly to cover early-return branch
    _prune_retained_logs(
        directory=tmp_path,
        patterns=("debug-*.log",),
        keep=5,
    )
    assert list(tmp_path.iterdir()) == []
