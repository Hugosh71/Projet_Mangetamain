"""Main entry point of the app."""

from pathlib import Path

import streamlit as st

from app.logging_config import configure_logging, get_logger

ROOT = Path(__file__).resolve().parents[1]


def _initialise_logging() -> None:
    configure_logging(log_directory=ROOT / "logs", reset_existing=True)


if __name__ == "__main__":
    _initialise_logging()
    logger = get_logger()
    logger.debug("Starting the application")

    home_page = st.Page("home.py", title="Accueil", icon=":material/home:")
    clustering_page = st.Page(
        "clustering.py", title="Clustering", icon=":material/graph_6:"
    )
    method_page = st.Page(
        "methodology.py", title="Méthodologie", icon=":material/book:"
    )

    # Create nav in side bar
    pg = st.navigation([home_page, clustering_page, method_page])
    pg.run()
