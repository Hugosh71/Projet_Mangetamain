"""Shared pytest fixtures."""

import pytest


@pytest.fixture(scope="session")
def sample_data_dir(tmp_path_factory):
    """Provide a temporary directory for sample data files."""

    return tmp_path_factory.mktemp("data")

