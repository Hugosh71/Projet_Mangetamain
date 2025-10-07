"""Page d'accueil de l'application"""

import streamlit as st
import plotly.express as px

from src.mangetamain import (
    get_top_recipes_cached,
    get_vegetarian_stats_cached,
)

st.set_page_config(page_title="Accueil", page_icon="📈", layout="wide")

top_recipes = get_top_recipes_cached(top_k=10)
vegetarian_stats = get_vegetarian_stats_cached()

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
    "Classées par note moyenne la plus élevée, puis par la plus faible variabilité, et "
    "enfin par le plus grand nombre d'évaluations."
)

st.dataframe(top_recipes, width="stretch")

st.subheader("📊 Analyse des recettes : Végétarien vs Viande")

col1, col2 = st.columns(2)

with col1:
    fig_pie = px.pie(
        vagetarian_stats,
        values="Nombre de recettes uniques",
        names="Type",
        title="Répartition des recettes (végétarien vs viande)",
        hole=0.4,  # effet donut
    )
    fig_pie.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    fig_bar = px.bar(
        vegetarian_stats,
        x="Type",
        y="Note moyenne",
        color="Type",
        title="Moyenne des notes (végétarien vs viande)",
        text="Note moyenne",
    )
    fig_bar.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    fig_bar.update_layout(
        yaxis_title="Note moyenne",
        xaxis_title="Catégorie",
        uniformtext_minsize=8,
        uniformtext_mode="hide",
    )
    st.plotly_chart(fig_bar, use_container_width=True)
