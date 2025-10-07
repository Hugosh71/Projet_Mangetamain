"""Centralized logging configuration for Mangetamain.

This module provides a robust logging setup that captures detailed
contextual information for both user actions and critical events. It
creates two dedicated log files per application run – one for DEBUG (and
above) messages and another limited to ERROR and CRITICAL entries. Each
log file name embeds the session timestamp, and a retention policy keeps
the total number of log files bounded.
"""

from __future__ import annotations

import logging
import os
import uuid
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from logging import handlers
from pathlib import Path

__all__ = [
    "configure_logging",
    "get_logger",
    "LoggingConfig",
]


BASE_LOGGER_NAME = "mangetamain"
LOG_DIR_NAME = "logs"
LOG_DEBUG_FILENAME_TEMPLATE = "debug-{timestamp}.log"
LOG_ERROR_FILENAME_TEMPLATE = "error-{timestamp}.log"
LOG_USER_ID = "MANG_USER_ID"
LOG_SESSION_ID = "MANG_SESSION_ID"
LOG_MAX_LOG_FILES = 10


@dataclass(frozen=True)
class LoggingConfig:
    """Configuration details returned by :func:`configure_logging`."""

    log_directory: Path
    debug_log_path: Path
    error_log_path: Path
    run_identifier: str
    run_timestamp: str


class _ContextFilter(logging.Filter):
    """Injects contextual information into log records."""

    def __init__(
        self,
        *,
        user_id: str | None,
        session_id: str | None,
        run_id: str,
        run_timestamp: str,
    ) -> None:
        super().__init__(name="")
        self._user_id = user_id or "anonymous"
        self._session_id = session_id or uuid.uuid4().hex
        self._run_id = run_id
        self._run_timestamp = run_timestamp

    def filter(self, record: logging.LogRecord) -> bool:  # noqa: D401
        record.user_id = getattr(record, "user_id", self._user_id)
        record.session_id = getattr(record, "session_id", self._session_id)
        record.run_id = self._run_id
        record.run_timestamp = self._run_timestamp
        return True


class _ContextFormatter(logging.Formatter):
    """Formatter that emits high fidelity timestamps and file locations."""

    default_msec_format = "%s.%03d"

    def __init__(self) -> None:
        fmt = (
            "%(timestamp)s | %(levelname)s | %(pathname)s:%(lineno)d | "
            "run=%(run_id)s | user=%(user_id)s | session=%(session_id)s | %(message)s"
        )
        super().__init__(fmt=fmt, style="%")

    def formatTime(self, record: logging.LogRecord, datefmt: str | None = None) -> str:
        dt = datetime.fromtimestamp(record.created, tz=UTC)
        return dt.isoformat(timespec="milliseconds")

    def format(self, record: logging.LogRecord) -> str:  # noqa: D401
        record.timestamp = self.formatTime(record)
        return super().format(record)


def configure_logging(
    *,
    log_directory: str | os.PathLike[str] | None = None,
    max_log_files: int | None = None,
    user_id: str | None = None,
    session_id: str | None = None,
) -> LoggingConfig:
    """Configure the application-wide logging stack.

    This function is idempotent – calling it multiple times will return the
    existing configuration without re-creating handlers. The first call will
    create two file handlers (debug and error-only) and enforce a retention
    policy that keeps the number of log files bounded.
    """

    logger = logging.getLogger(BASE_LOGGER_NAME)
    if getattr(logger, "__mangetamain_configured__", False):
        # Return the existing configuration captured on the first setup.
        return logger.__mangetamain_logging_config__  # type: ignore[attr-defined]

    # Utiliser les variables d'environnement si les paramètres ne sont pas fournis
    if log_directory is None:
        log_directory = os.path.join(os.path.dirname(__file__), LOG_DIR_NAME)
    if user_id is None:
        user_id = LOG_USER_ID
    if session_id is None:
        session_id = LOG_SESSION_ID
    if max_log_files is None:
        max_log_files = LOG_MAX_LOG_FILES
        if max_log_files is not None:
            try:
                max_log_files = int(max_log_files)
            except ValueError:
                max_log_files = None

    resolved_log_dir = _resolve_log_directory(log_directory)
    resolved_log_dir.mkdir(parents=True, exist_ok=True)

    max_files = _resolve_max_files(max_log_files)

    run_timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    run_id = uuid.uuid4().hex

    debug_log_path = resolved_log_dir / LOG_DEBUG_FILENAME_TEMPLATE.format(
        timestamp=run_timestamp
    )
    error_log_path = resolved_log_dir / LOG_ERROR_FILENAME_TEMPLATE.format(
        timestamp=run_timestamp
    )

    debug_handler = _build_file_handler(debug_log_path, level=logging.DEBUG)
    error_handler = _build_file_handler(error_log_path, level=logging.ERROR)

    formatter = _ContextFormatter()
    debug_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)

    context_filter = _ContextFilter(
        user_id=user_id,
        session_id=session_id,
        run_id=run_id,
        run_timestamp=run_timestamp,
    )

    # Ajouter le filtre aux handlers pour s'assurer qu'il est appliqué avant le formatage
    debug_handler.addFilter(context_filter)
    error_handler.addFilter(context_filter)

    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    logger.addHandler(debug_handler)
    logger.addHandler(error_handler)

    _prune_retained_logs(
        directory=resolved_log_dir,
        patterns=("debug-*.log", "error-*.log"),
        keep=max_files,
    )

    logging_config = LoggingConfig(
        log_directory=resolved_log_dir,
        debug_log_path=debug_log_path,
        error_log_path=error_log_path,
        run_identifier=run_id,
        run_timestamp=run_timestamp,
    )

    logger.__mangetamain_configured__ = True  # type: ignore[attr-defined]
    logger.__mangetamain_logging_config__ = logging_config  # type: ignore[attr-defined]

    return logging_config


def get_logger(name: str | None = None) -> logging.Logger:
    """Return a logger that inherits the Mangetamain logging configuration."""

    if name:
        return logging.getLogger(f"{BASE_LOGGER_NAME}.{name}")
    return logging.getLogger(BASE_LOGGER_NAME)


def _build_file_handler(path: Path, *, level: int) -> logging.Handler:
    handler = (
        handlers.WatchedFileHandler(path)
        if os.name != "nt"
        else logging.FileHandler(path, encoding="utf-8")
    )
    handler.setLevel(level)
    return handler


def _resolve_log_directory(directory: str | os.PathLike[str] | None) -> Path:
    if directory is not None:
        return Path(directory).expanduser().resolve()
    return Path(__file__).resolve().parents[2] / LOG_DIR_NAME


def _resolve_max_files(max_log_files: int | None) -> int:
    if max_log_files is not None:
        return max(1, max_log_files)

    raw_value = os.environ.get(LOG_MAX_LOG_FILES)
    if raw_value is None:
        return LOG_MAX_LOG_FILES

    try:
        return max(1, int(raw_value))
    except ValueError:
        return LOG_MAX_LOG_FILES


def _prune_retained_logs(
    *, directory: Path, patterns: Iterable[str], keep: int
) -> None:
    seen: dict[Path, Path] = {}
    for pattern in patterns:
        for path in directory.glob(pattern):
            seen[path.resolve()] = path

    if not seen:
        return

    ordered = sorted(
        seen.values(), key=lambda candidate: candidate.stat().st_mtime, reverse=True
    )
    for obsolete in ordered[keep:]:
        try:
            obsolete.unlink(missing_ok=True)
        except OSError:
            continue
