"""Project-wide configuration helpers for environment-driven settings."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Final


PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parents[2]
DEFAULT_LOG_DIR_NAME: Final[str] = "logs"
DEFAULT_LOG_DIR: Final[Path] = PROJECT_ROOT / DEFAULT_LOG_DIR_NAME
DEFAULT_MAX_LOG_FILES: Final[int] = 10

ENV_LOG_DIR: Final[str] = "MANG_LOG_DIR"
ENV_LOG_MAX_FILES: Final[str] = "MANG_LOG_MAX_FILES"
ENV_USER_ID: Final[str] = "MANG_USER_ID"
ENV_SESSION_ID: Final[str] = "MANG_SESSION_ID"


def load_env_file(
    path: str | os.PathLike[str] | None = None,
    *,
    override: bool = False,
) -> None:
    """Populate ``os.environ`` from a ``.env`` style file if it exists."""

    candidate = Path(path) if path is not None else PROJECT_ROOT / ".env"
    if not candidate.exists():
        return

    for raw_line in candidate.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        key, sep, value = line.partition("=")
        if not sep:
            continue

        key = key.strip()
        value = value.strip()

        if value.startswith(("'", '"')) and value.endswith(("'", '"')):
            value = value[1:-1]

        if override or key not in os.environ:
            os.environ[key] = value


@dataclass(frozen=True)
class LoggingSettings:
    """Materialised logging configuration derived from environment values."""

    directory: Path
    user_id: str | None
    session_id: str | None
    max_files: int

    @classmethod
    def from_env(cls) -> "LoggingSettings":
        """Create logging settings using environment variables or defaults."""

        load_env_file()

        directory = _resolve_directory(os.getenv(ENV_LOG_DIR))
        user_id = os.getenv(ENV_USER_ID)
        session_id = os.getenv(ENV_SESSION_ID)
        max_files = _parse_positive_int(os.getenv(ENV_LOG_MAX_FILES), DEFAULT_MAX_LOG_FILES)

        return cls(directory=directory, user_id=user_id, session_id=session_id, max_files=max_files)


def _resolve_directory(raw: str | None) -> Path:
    if not raw:
        return DEFAULT_LOG_DIR

    candidate = Path(raw).expanduser()
    if not candidate.is_absolute():
        candidate = (PROJECT_ROOT / candidate).resolve()
    else:
        candidate = candidate.resolve()
    return candidate


def _parse_positive_int(raw: str | None, default: int) -> int:
    if raw is None or raw == "":
        return default

    try:
        value = int(raw)
    except ValueError:
        return default

    return max(1, value)

