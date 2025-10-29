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

from .settings import DEFAULT_MAX_LOG_FILES, LoggingSettings

__all__ = [
    "configure_logging",
    "get_logger",
    "reset_logging",
    "LoggingConfig",
]


BASE_LOGGER_NAME = "mangetamain"
LOG_DEBUG_FILENAME_TEMPLATE = "debug-{timestamp}.log"
LOG_ERROR_FILENAME_TEMPLATE = "error-{timestamp}.log"


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
            "%(timestamp)s | %(levelname)s | "
            "%(pathname)s:%(lineno)d | run=%(run_id)s | "
            "user=%(user_id)s | session=%(session_id)s | "
            "%(message)s"
        )
        super().__init__(fmt=fmt, style="%")

    def formatTime(
        self,
        record: logging.LogRecord,
        datefmt: str | None = None,
    ) -> str:
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
    reset_existing: bool = False,
) -> LoggingConfig:
    """Configure the application-wide logging stack.

    This function is idempotent – calling it multiple times will return the
    existing configuration without re-creating handlers. The first call will
    create two file handlers (debug and error-only) and enforce a retention
    policy that keeps the number of log files bounded.
    """

    logger = logging.getLogger(BASE_LOGGER_NAME)
    if reset_existing and getattr(logger, "__mangetamain_configured__", False):
        reset_logging()

    if getattr(logger, "__mangetamain_configured__", False):
        # Return the existing configuration captured on the first setup.
        existing = getattr(logger, "__mangetamain_logging_config__")
        return existing  # type: ignore[attr-defined]

    derived = LoggingSettings.from_env()

    if log_directory is None:
        log_directory = derived.directory
    if user_id is None:
        user_id = derived.user_id
    if session_id is None:
        session_id = derived.session_id
    if max_log_files is None:
        max_log_files = derived.max_files

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
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = _ContextFormatter()
    debug_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    context_filter = _ContextFilter(
        user_id=user_id,
        session_id=session_id,
        run_id=run_id,
        run_timestamp=run_timestamp,
    )

    # Ajouter le filtre aux handlers pour s'assurer qu'il est appliqué
    # avant le formatage
    debug_handler.addFilter(context_filter)
    error_handler.addFilter(context_filter)
    console_handler.addFilter(context_filter)

    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    logger.addHandler(debug_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)

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
    setattr(logger, "__mangetamain_logging_config__", logging_config)

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


def _resolve_log_directory(directory: str | Path | None) -> Path:
    if directory is None:
        return LoggingSettings.from_env().directory

    if isinstance(directory, Path):
        candidate = directory
    else:
        candidate = Path(directory)

    return candidate.expanduser().resolve()


def _resolve_max_files(max_log_files: int | None) -> int:
    if max_log_files is None:
        return DEFAULT_MAX_LOG_FILES

    return max(1, max_log_files)


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
        seen.values(),
        key=lambda candidate: candidate.stat().st_mtime,
        reverse=True,
    )
    for obsolete in ordered[keep:]:
        try:
            obsolete.unlink(missing_ok=True)
        except OSError:
            continue


def reset_logging() -> None:
    """Remove handlers and cached configuration for the Mangetamain logger."""

    logger = logging.getLogger(BASE_LOGGER_NAME)

    for handler in list(logger.handlers):
        handler.close()
        logger.removeHandler(handler)

    logger.filters.clear()

    if hasattr(logger, "__mangetamain_configured__"):
        delattr(logger, "__mangetamain_configured__")

    if hasattr(logger, "__mangetamain_logging_config__"):
        delattr(logger, "__mangetamain_logging_config__")
