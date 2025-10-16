"""Page d'accueil de l'application"""

import plotly.express as px
import streamlit as st

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

st.subheader("Analyse des recettes par catégorie : végétarien 🥦 vs. viande 🍖")

col1, col2 = st.columns(2)

with col1:
    fig_pie = px.pie(
        vegetarian_stats["stats"],
        values="unique_recipes",
        names="type",
        color="type",
        title="Répartition des recettes (végétarien vs. viande)",
        hole=0.4,
        color_discrete_map={
            "végétarien": "#00CC96",
            "viande": "#EF553B",
            "autre": "#636EFA",
        },
    )
    fig_pie.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    fig_bar = px.bar(
        vegetarian_stats["stats"],
        x="type",
        y="mean_rating",
        color="type",
        title="Moyenne des notes (végétarien vs. viande)",
        text="mean_rating",
        color_discrete_map={
            "végétarien": "#00CC96",
            "viande": "#EF553B",
            "autre": "#636EFA",
        },
    )
    fig_bar.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    fig_bar.update_layout(
        yaxis_title="Note moyenne",
        xaxis_title="Catégorie",
        uniformtext_minsize=8,
        uniformtext_mode="hide",
    )
    st.plotly_chart(fig_bar, use_container_width=True)

df_long = vegetarian_stats["monthly_ratios"].melt(
    id_vars="month",
    value_vars=["autre", "viande", "végétarien"],
    var_name="Type",
    value_name="Ratio",
)

# Create stacked bar chart
fig = px.bar(
    df_long,
    x="month",
    y="Ratio",
    color="Type",
    barmode="stack",  # 🔸 stacked bar mode
    title="📊 Ratio des types de recettes par mois",
    color_discrete_map={
        "végétarien": "#00CC96",
        "viande": "#EF553B",
        "autre": "#636EFA",
    },
)

# Beautify layout
fig.update_layout(
    xaxis=dict(
        tickmode="array",
        tickvals=list(range(1, 13)),
        ticktext=[
            "Jan",
            "Fév",
            "Mar",
            "Avr",
            "Mai",
            "Juin",
            "Juil",
            "Août",
            "Sep",
            "Oct",
            "Nov",
            "Déc",
        ],
    ),
    yaxis_tickformat=".0%",
    yaxis_title="Ratio",
    xaxis_title="Mois",
    legend_title_text="Type",
)

st.plotly_chart(fig, use_container_width=True)
