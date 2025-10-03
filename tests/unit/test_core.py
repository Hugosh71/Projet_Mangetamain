"""Unit tests for core utilities."""

from mangetamain.core import AppConfig, get_app_config


def test_get_app_config_returns_defaults():
    config = get_app_config()

    assert isinstance(config, AppConfig)
    assert config.name == "Mangetamain"
    assert config.version == "0.1.0"
