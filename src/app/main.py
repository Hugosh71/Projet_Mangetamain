"""Main entry point of the app."""

import streamlit as st

from src.mangetamain.logging_config import configure_logging, get_logger


def _initialise_logging() -> None:
    configure_logging(log_directory="./logs", reset_existing=True)


if __name__ == "__main__":
    _initialise_logging()
    logger = get_logger()
    logger.debug("Starting the application")

    home_page = st.Page("home.py", title="Home", icon=":material/home:")
    clustering_page = st.Page(
        "clustering.py", title="Clustering", icon=":material/add_circle:"
    )

    pg = st.navigation([home_page, clustering_page])
    pg.run()
