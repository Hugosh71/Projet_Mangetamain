"""Page d'accueil de l'application"""

import streamlit as st

st.set_page_config(page_title="Accueil", page_icon="📈", layout="wide")

st.markdown("# Accueil")
st.sidebar.header("Accueil")

st.markdown(
    """
    Bienvenue sur **Mangetamain** !
    
    Cette application est conçue pour vous aider à explorer des recettes saines.
    """
)
