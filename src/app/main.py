"""Main entry point of the app."""

import streamlit as st

if __name__ == "__main__":
    home_page = st.Page("home.py", title="Accueil", icon=":material/home:")
    clustering_page = st.Page(
        "clustering.py", title="Clustering", icon=":material/graph_6:"
    )

    pg = st.navigation([home_page, clustering_page])
    pg.run()
