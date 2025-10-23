"""Clustering visualization page for recipe analysis."""

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import streamlit as st

from src.mangetamain.preprocessing.streamlit import (
    add_month_labels,
    get_cluster_names,
    get_col_names,
    load_recipes_data,
    min_max_scale,
    remove_outliers_iqr,
    rgb_to_hex,
    get_tag_cloud,
    get_cluster_summary,
)

# Set Streamlit page configuration
st.set_page_config(
    page_title="Analyse de clusters des recettes", page_icon="🍽️", layout="wide"
)

st.markdown("# Analyse de Clusters des Recettes")
st.sidebar.markdown("")

# Load data and cluster names
df_recipes = load_recipes_data()
cluster_names = get_cluster_names()
df_recipes["cluster_name"] = df_recipes["cluster"].map(cluster_names)
colors = px.colors.qualitative.Set2
color_map = {
    cn: rgb_to_hex(colors[i % len(colors)])
    for i, cn in enumerate(cluster_names.values())
}

st.markdown("### Comparaison des Clusters de Recettes")

# Cluster selection pills
clusters = sorted(df_recipes["cluster"].unique())
selected_clusters = st.pills(
    "Sélectionnez les clusters à comparer :",
    cluster_names.values(),
    default=cluster_names.values(),
    selection_mode="multi",
)

if not selected_clusters:
    st.warning(
        "Vous devez sélectionner au moins un cluster.", icon=":material/warning:"
    )

df_recipes_filtered = df_recipes[df_recipes["cluster_name"].isin(selected_clusters)]

col_scatter, col_pie = st.columns([2, 1])

#################################################
# Scatter plot of PCA components
#################################################
with col_scatter.container(border=True, height="stretch"):
    fig = px.scatter(
        remove_outliers_iqr(df_recipes_filtered, ["pc_1", "pc_2"]),
        x="pc_1",
        y="pc_2",
        color="cluster_name",
        hover_data=["name"],
        title="Clusters de recettes dans l'espace PCA (2D)",
        labels={"pc_1": "Composante principale 1", "pc_2": "Composante principale 2"},
        color_discrete_map=color_map,
        template="simple_white",
        size_max=10,
    )
    fig.update_layout(
        title={"x": 0},
        margin={"t": 50, "b": 0, "l": 0, "r": 0},
        legend_title="Cluster",
    )

    st.plotly_chart(fig, use_container_width=True)

#################################################
# Pie chart of recipe distribution by cluster
#################################################
with col_pie.container(border=True, height="stretch"):
    cluster_counts = (
        df_recipes_filtered["cluster_name"]
        .value_counts()
        .reindex(cluster_names.values(), fill_value=0)
    )

    fig_pie = px.pie(
        values=cluster_counts.values,
        names=cluster_counts.index,
        title="Distribution des recettes par cluster",
        color=cluster_counts.index,
        color_discrete_map=color_map,
        template="simple_white",
    )

    fig_pie.update_traces(
        textposition="inside",
        textinfo="percent+label",
        textfont_size=12,
        pull=[0.01] * len(cluster_counts),
        domain={"x": [0.15, 0.85], "y": [0.15, 0.85]},
    )

    fig_pie.update_layout(
        title={"x": 0, "xanchor": "left"},
        showlegend=False,
        margin={"l": 10, "r": 0, "t": 50, "b": 0},
        legend_title="Cluster",
    )

    st.plotly_chart(fig_pie, use_container_width=True)

#################################################
# Box plots of favor scores by cluster
#################################################
with st.container(border=True, height="stretch"):
    st.markdown("**Scores faveur par cluster**")
    cols_favor = [
        "score_sweet_savory",
        "score_spicy_mild",
        "score_lowcal_rich",
        "score_vegetarian_meat",
        "score_solid_liquid",
        "score_raw_processed",
        "score_western_exotic",
    ]

    df_melted = min_max_scale(df_recipes_filtered, cols_favor).melt(
        id_vars="cluster_name",
        value_vars=cols_favor,
        var_name="Faveur",
        value_name="Score",
    )
    df_melted["Faveur"] = df_melted["Faveur"].map(get_col_names(cols_favor))

    fig = px.box(
        df_melted,
        x="Faveur",
        y="Score",
        color="cluster_name",
        color_discrete_map=color_map,
        template="simple_white",
        points="outliers",  # Show outliers
    )

    fig.update_layout(
        title="",
        title_x=0,
        xaxis_title="Faveur",
        yaxis_title="Score (normalisé)",
        boxmode="group",  # Group the boxes together by cluster
        height=500,
        margin={"l": 20, "r": 20, "t": 50, "b": 50},
        legend_title="Cluster",
    )

    st.plotly_chart(fig, use_container_width=True)

col_nutrition, col_seasonality = st.columns([2, 1])

###############################################################
# Radar chart of average nutritional characteristics by cluster
###############################################################
with col_nutrition.container(border=True, height="stretch"):
    st.markdown("**Caractéristiques nutritionnelles moyennes**")
    metrics = ["energy_density", "protein_ratio", "fat_ratio", "nutrient_balance_index"]
    df_recipes_nutrition = min_max_scale(
        df_recipes_filtered[["cluster_name", *metrics]], metrics
    )
    df_cluster_mean = (
        df_recipes_nutrition.groupby("cluster_name")[metrics].mean().reset_index()
    )
    df_melted = df_cluster_mean.melt(
        id_vars="cluster_name", var_name="metric", value_name="value"
    )
    fig = px.line_polar(
        df_melted,
        r="value",
        theta="metric",
        color="cluster_name",
        line_close=True,
        markers=True,
        color_discrete_map=color_map,
        template="plotly_white",
    )
    fig.update_traces(fill="toself", opacity=0.6)
    fig.update_layout(title="", title_x=0, height=400, legend_title="Cluster")

    st.plotly_chart(fig, use_container_width=True)

#################################################
# Seasonality scatter plot
#################################################
with col_seasonality.container(border=True, height="stretch"):
    st.markdown("**Position saisonnière des interactions (lissée)**")

    fig, ax = plt.subplots(figsize=(6, 6))

    colors = df_recipes_filtered["cluster_name"].map(color_map).values
    ax.scatter(
        df_recipes_filtered["inter_doy_cos_smooth"],
        df_recipes_filtered["inter_doy_sin_smooth"],
        s=10,
        alpha=0.4,
        color=colors,
    )
    circle = plt.Circle((0, 0), 1, color="grey", fill=False, linestyle="--")
    ax.add_artist(circle)
    ax.axhline(0, color="grey", lw=0.5)
    ax.axvline(0, color="grey", lw=0.5)

    ax.set_aspect("equal", "box")
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_title("")
    ax.set_xlabel("cosinus du jour de l'année (interaction)")
    ax.set_ylabel("sinus du jour de l'année (interaction)")

    add_month_labels(ax)

    fig.tight_layout()
    st.pyplot(fig, use_container_width=False)

col_rating, col_time = st.columns([1, 1])

######################################################
# Bar chart of average ratings distribution by cluster
######################################################
with col_rating.container(border=True, height="stretch"):
    st.markdown("**Distribution des notes moyennes**")
    bins = [1, 2, 3, 4, 5]
    df_binned = df_recipes_filtered.copy()
    df_binned["rating_bin"] = pd.cut(
        df_binned["rating_mean"], bins=bins, include_lowest=True
    )

    df_binned["rating_bin"] = df_binned["rating_bin"].apply(
        lambda x: f"{x.left:.1f}–{x.right:.1f}" if pd.notnull(x) else "NA"
    )

    df_counts = (
        df_binned.groupby(["rating_bin", "cluster_name"])
        .size()
        .reset_index(name="count")
    )

    fig = px.bar(
        df_counts,
        x="rating_bin",
        y="count",
        color="cluster_name",
        barmode="group",
        color_discrete_map=color_map,
        template="simple_white",
    )

    fig.update_layout(
        title="",
        title_x=0,
        xaxis_title="Note moyenne",
        yaxis_title="Nombre de recettes",
        height=300,
        margin={"l": 40, "r": 20, "t": 50, "b": 40},
        legend_title="Cluster",
    )

    fig.update_xaxes(categoryorder="category ascending")

    st.plotly_chart(fig, use_container_width=True, key="multi_series_bar_chart")

######################################################
# Bar chart of average preparation time by cluster
######################################################

with col_time.container(border=True, height="stretch"):
    st.markdown("**Durée de préparation des recettes**")

st.markdown("### Exploration des Recettes par Cluster")

##################################################
# Cluster exploration section
##################################################
# Create dropdown with cluster names
selected_cluster = st.selectbox(
    "Sélectionnez un cluster à explorer :",
    options=clusters,
    format_func=lambda x: f"Cluster {x} : {cluster_names[x]}",
    help="Choose a cluster to see its recipes, ingredients, and tags",
)

# Filter data for selected cluster
cluster_data = df_recipes[df_recipes["cluster"] == selected_cluster].copy()

col_metric_1, col_metric_2, col_metric_3 = st.columns([1, 2, 1])

cluster_summary = get_cluster_summary(cluster_data, selected_cluster)

with col_metric_1.container(border=True, height="stretch"):
    # Display cluster information
    st.metric(
        label="Nombre de recettes", value=f"{cluster_summary['n']:,.0f}", delta=None
    )
    st.metric(
        label="Nombre moyen d'étapes",
        value=f"{cluster_summary['n_steps_mean']:.0f}",
        delta=None,
    )
    st.metric(
        label="Durée de préparation (minutes)",
        value=f"{cluster_summary['minutes_mean']:.0f}",
        delta=None,
    )

with col_metric_2.container(border=True, height="stretch"):
    if selected_cluster == 0:
        st.markdown(
            """
<div style="font-size:14px; line-height:1.5;">
<p><strong>Description du cluster</strong></p>
<strong>Recettes longues, équilibrées, riches en protéines — type plats principaux familiaux</strong>
<ul>
<li>Énergie modérée : 4.8 kcal/g</li>
<li>Bon ratio protéines (0.12), lipides modérés (0.07)</li>
<li>Indice nutritionnel positif (0.036) : plutôt équilibré</li>
<li>Recettes assez longues : ~82 minutes</li>
<li>Beaucoup d’étapes et d’ingrédients (n_steps_z = +0.77, n_ingredients_z = +1.12)</li>
<li>Saveur neutre-salée, peu sucrée (0.035)</li>
<li>Légèrement solide, un peu transformée (0.05)</li>
</ul>
</div>
            """,
            unsafe_allow_html=True,
        )
    elif selected_cluster == 1:
        st.markdown(
            """
<div style="font-size:14px; line-height:1.5;">
<p><strong>Description du cluster</strong></p>
<strong>Recettes faciles, équilibrées, plutôt salées et rapides — plats du quotidien</strong>
<ul>
<li>Énergie similaire (4.93 kcal/g)</li>
<li>Protéines et graisses modérées, indice nutritionnel plus faible (0.021)</li>
<li>Recettes plus rapides (~40 minutes)</li>
<li>Moins d’ingrédients et d’étapes</li>
<li>Profil gustatif doux et salé, un peu plus épicé</li>
</ul>
</div>
""",
            unsafe_allow_html=True,
        )
    elif selected_cluster == 2:
        st.markdown(
            """
<div style="font-size:14px; line-height:1.5;">
<p><strong>Description du cluster</strong></p>
<strong>Peu de protéines, plus caloriques, sucrées — desserts, pâtisseries, douceurs</strong>
<ul>
<li>Énergie plus élevée (6.9 kcal/g)</li>
<li>Peu de protéines (0.033)</li>
<li>Indice nutritionnel négatif (-0.106)</li>
<li>Durée moyenne (~48 minutes)</li>
<li>Saveur sucrée prononcée (0.13)</li>
<li>Légèrement transformé (0.063)</li>
<li>Assez “exotique” (0.054)</li>
</ul>
</div>
""",
            unsafe_allow_html=True,
        )
    elif selected_cluster == 3:
        st.markdown(
            """
<div style="font-size:14px; line-height:1.5;">
<p><strong>Description du cluster</strong></p>
<strong>Densité énergétique très haute, faible qualité nutritionnelle — gâteaux, barres, confiseries</strong>
<ul>
<li>Très énergétique (15.75 kcal/g)</li>
<li>Très pauvres en protéines et lipides (faible densité nutritionnelle)</li>
<li>Indice nutritionnel très négatif (-0.513)</li>
<li>Recettes rapides (~13 minutes)</li>
<li>Très sucrées (0.15) et peu salées, plus transformées (0.10)</li>
<li>Très simples, peu d’ingrédients</li>
</ul>
</div>
""",
            unsafe_allow_html=True,
        )
    elif selected_cluster == 4:
        st.markdown(
            """
<div style="font-size:14px; line-height:1.5;">
<p><strong>Description du cluster</strong></p>
<strong>Recettes ni trop longues ni trop riches, un peu transformées — plats rapides ou préparations express</strong>
<ul>
<li>Énergie modérée (5.42 kcal/g)</li>
<li>Protéines faibles (0.083), graisses modérées (0.078)</li>
<li>Indice nutritionnel légèrement négatif (-0.045)</li>
<li>Temps moyen (~23 minutes)</li>
<li>Assez équilibré en goût, légèrement sucré/salé, plutôt transformé (0.068)</li>
</ul>
</div>
""",
            unsafe_allow_html=True,
        )


with col_metric_3.container(border=True, height="stretch"):
    st.markdown(
        '<strong style="font-size:14px;">Top tags</strong>',
        unsafe_allow_html=True,
    )
    wordcloud = get_tag_cloud(
        cluster_data,
        tag_col="tags",
        use_tfidf=True,
    )
    fig, ax = plt.subplots(figsize=(15, 15))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig, use_container_width=False)

st.markdown("**Détails des recettes du cluster sélectionné**")
##################################################
# Recipe details dataframe
##################################################
if not cluster_data.empty:
    # Select available columns for display
    display_cols = [
        "id",
        "name",
        "minutes",
        "n_steps",
        "n_ingredients",
        "score_sweet_savory",
        "score_spicy_mild",
        "score_lowcal_rich",
        "score_vegetarian_meat",
        "score_solid_liquid",
        "score_raw_processed",
        "score_western_exotic",
        "energy_density",
        "protein_ratio",
        "fat_ratio",
        "nutrient_balance_index",
        "rating_mean",
    ]
    col_names = get_col_names(display_cols, return_values=True)

    # Create display dataframe
    display_data = cluster_data[display_cols].copy()
    display_data.columns = col_names

    # Create column configuration
    column_config = {}
    for i, col in enumerate(display_cols):
        col_name = col_names[i]
        if col == "id":
            column_config[col_name] = st.column_config.NumberColumn(
                col_name, width="small"
            )
        elif col in ["name"]:
            column_config[col_name] = st.column_config.TextColumn(
                col_name, width="medium"
            )
        else:
            column_config[col_name] = st.column_config.TextColumn(
                col_name, width="medium"
            )

    st.dataframe(
        display_data,
        width="content",
        hide_index=True,
        column_config=column_config,
    )
else:
    st.warning("No recipes found for the selected cluster.")
