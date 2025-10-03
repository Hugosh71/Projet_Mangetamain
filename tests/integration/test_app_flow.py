"""Integration-level tests for Streamlit app flow."""

from mangetamain.core import get_app_config


def test_app_config_loaded():
    config = get_app_config()

    assert config.name == "Mangetamain"
