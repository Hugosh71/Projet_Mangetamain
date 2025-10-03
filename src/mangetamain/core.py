"""Core utilities for Mangetamain."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    """Base configuration for the application."""

    name: str = "Mangetamain"
    version: str = "0.1.0"


def get_app_config() -> AppConfig:
    """Return default app configuration."""

    return AppConfig()
