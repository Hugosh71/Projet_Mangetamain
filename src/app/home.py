"""Page d'accueil de l'application — version optimisée."""

import streamlit as st
from mangetamain import DataPreprocessor
import os

# ✅ Configurer la page en premier
st.set_page_config(page_title="Accueil", page_icon="📈", layout="wide")

preprocessor = DataPreprocessor()

# Utiliser le cache disque de Streamlit (persistant dans .streamlit/cache)
from mangetamain import get_top_recipes_cached

top_recipes = get_top_recipes_cached(
    recipes_csv=preprocessor.data_paths.recipes_csv,
    interactions_csv=preprocessor.data_paths.interactions_csv,
    top_k=10,
)

# ✅ Interface Streamlit
st.markdown("# Accueil")
st.sidebar.header("Accueil")

st.markdown(
    """
    Bienvenue sur **Mangetamain** !
    
    Cette application est conçue pour vous aider à explorer des recettes saines.
    """
)

st.subheader("Recettes les mieux notées")
st.caption(
    "Classées par note moyenne la plus élevée, puis par la plus faible variabilité, et enfin par le plus grand nombre d'évaluations."
)

st.dataframe(top_recipes, width="stretch")
