"""Main entry point of the app."""

import streamlit as st

from mangetamain.logging_config import configure_logging

def _initialise_logging() -> None:
    configure_logging(reset_existing=True)


if __name__ == "__main__":
    _initialise_logging()

    home_page = st.Page("home.py", title="Home", icon=":material/home:")
    clustering_page = st.Page(
        "clustering.py", title="Clustering", icon=":material/add_circle:"
    )

    pg = st.navigation([home_page, clustering_page])
    pg.run()
