"""Main entry point of the app."""
import sys
from pathlib import Path

# Ajouter "src" au chemin des modules
sys.path.append(str(Path(__file__).resolve().parents[1]))  # remonte 2 niveaux → src

import streamlit as st

if __name__ == "__main__":
    home_page = st.Page("home.py", title="Home", icon=":material/home:")
    clustering_page = st.Page(
        "clustering.py", title="Clustering", icon=":material/add_circle:"
    )

    pg = st.navigation([home_page, clustering_page])
    pg.run()
