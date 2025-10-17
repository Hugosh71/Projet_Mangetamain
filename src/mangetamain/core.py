"""Core utilities for Mangetamain.

This module provides essential configuration and utility functions for the
Mangetamain application. It includes the main configuration class and
helper functions for application setup.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    """Application configuration container.

    This class holds the core configuration settings for the Mangetamain
    application. It uses a frozen dataclass to ensure immutability and
    type safety.

    Attributes:
        name (str): The name of the application. Defaults to "Mangetamain".
        version (str): The version of the application. Defaults to "0.1.0".

    Example:
        >>> config = AppConfig()
        >>> print(config.name)
        Mangetamain
        >>> print(config.version)
        0.1.0

        >>> custom_config = AppConfig(name="MyApp", version="1.0.0")
        >>> print(custom_config.name)
        MyApp
    """

    name: str = "Mangetamain"
    version: str = "0.1.0"


def get_app_config() -> AppConfig:
    """Return the default application configuration.

    This function creates and returns a new AppConfig instance with
    default values. It serves as the primary way to access application
    configuration throughout the codebase.

    Returns:
        AppConfig: A new AppConfig instance with default values.

    Example:
        >>> config = get_app_config()
        >>> isinstance(config, AppConfig)
        True
        >>> config.name
        'Mangetamain'
        >>> config.version
        '0.1.0'
    """
    return AppConfig()
