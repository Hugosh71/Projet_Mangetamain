"""Clustering visualization page for recipe analysis."""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
from collections import Counter
import sys
import os

from src.mangetamain.preprocessing.streamlit import (
    load_recipes_data,
    get_cluster_names,
    get_data_summary,
    remove_outliers_iqr,
    add_month_labels,
    rgb_to_hex,
)

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

# # Check if data loaded successfully
# if df.empty:
#     st.error("❌ Failed to load data. Please check the data files.")
#     st.stop()

# # Get data summary
# summary = get_data_summary(df)

# # Overview section with modern styling
# st.markdown("## 📊 Dataset Overview")

# # Key numbers in one row
# col1, col2, col3, col4 = st.columns(4)
# with col1:
#     st.metric(
#         label="📈 Average Metric 1",
#         value=f"{summary['metric_1_mean']:.2f}",
#         delta=None
#     )
# with col2:
#     st.metric(
#         label="⏱️ Average Metric 2",
#         value=f"{summary['metric_2_mean']:.2f}",
#         delta=None
#     )
# with col3:
#     st.metric(
#         label="🍽️ Total Recipes",
#         value=f"{summary['total_recipes']:,}",
#         delta=None
#     )
# with col4:
#     st.metric(
#         label="🎯 Total Clusters",
#         value=f"{summary['total_clusters']}",
#         delta=None
#     )

# # Distributions by cluster with modern styling

st.markdown("### Comparaison des Clusters de Recettes")

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

# col_a, col_b = st.columns(2)

# with col_a:
#     if 'metric_1' in df.columns:
#         m1_by_cluster = df.groupby('cluster', as_index=False)['metric_1'].mean()
#         fig_m1 = px.bar(
#             m1_by_cluster,
#             x='cluster',
#             y='metric_1',
#             title='📈 Metric 1 by Cluster',
#             color='metric_1',
#             color_continuous_scale='viridis',
#             template='plotly_white'
#         )
#         fig_m1.update_layout(
#             xaxis_title="Cluster ID",
#             yaxis_title="Average Metric 1",
#             showlegend=False,
#             height=400
#         )
#         st.plotly_chart(fig_m1, use_container_width=True)

# with col_b:
#     if 'metric_2' in df.columns:
#         m2_by_cluster = df.groupby('cluster', as_index=False)['metric_2'].mean()
#         fig_m2 = px.bar(
#             m2_by_cluster,
#             x='cluster',
#             y='metric_2',
#             title='⏱️ Metric 2 by Cluster',
#             color='metric_2',
#             color_continuous_scale='plasma',
#             template='plotly_white'
#         )
#         fig_m2.update_layout(
#             xaxis_title="Cluster ID",
#             yaxis_title="Average Metric 2",
#             showlegend=False,
#             height=400
#         )
#         st.plotly_chart(fig_m2, use_container_width=True)

# Create two columns for scatter plot and pie chart
col_scatter, col_pie = st.columns([2, 1])

df_recipes_filtered = df_recipes[df_recipes["cluster_name"].isin(selected_clusters)]

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
    )

    st.plotly_chart(fig, use_container_width=True)

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
    )

    st.plotly_chart(fig_pie, use_container_width=True)

col_comp_seasonality, _, __ = st.columns([1, 1, 1])

with col_comp_seasonality.container(border=True, height="stretch"):
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

st.markdown("### Exploration des Recettes par Cluster")

# Create dropdown with cluster names
selected_cluster = st.selectbox(
    "Sélectionnez un cluster à explorer :",
    options=clusters,
    format_func=lambda x: f"Cluster {x} : {cluster_names[x]}",
    help="Choose a cluster to see its recipes, ingredients, and tags",
)

# Filter data for selected cluster
cluster_data = df_recipes[df_recipes["cluster"] == selected_cluster].copy()

# Display cluster information with modern styling
st.metric(label="Nombre de recettes", value=f"{len(cluster_data):,}", delta=None)


# Helper function for token frequencies
def top_token_frequencies(series: pd.Series, top_n: int = 15) -> pd.DataFrame:
    tokens: Counter = Counter()
    for s in series.dropna().astype(str):
        parts = [p.strip().lower() for p in s.split(",") if p.strip()]
        tokens.update(parts)
    most_common = tokens.most_common(top_n)
    return pd.DataFrame(most_common, columns=["token", "count"])


# Ingredients and Tags clouds for selected cluster
if not cluster_data.empty:
    col_ing, col_tag = st.columns(2)

    with col_ing:
        if "ingredients_clean" in cluster_data.columns:
            ing_df = top_token_frequencies(cluster_data["ingredients_clean"], top_n=15)
            if not ing_df.empty:
                cluster_name = cluster_names.get(
                    selected_cluster, f"Cluster {selected_cluster}"
                )
                fig_ing = px.bar(
                    ing_df,
                    x="count",
                    y="token",
                    orientation="h",
                    title=f"🥘 Top Ingredients in {cluster_name}",
                    color="count",
                    color_continuous_scale="blues",
                    template="plotly_white",
                )
                fig_ing.update_layout(
                    xaxis_title="Frequency",
                    yaxis_title="Ingredients",
                    height=400,
                    showlegend=False,
                )
                st.plotly_chart(fig_ing, use_container_width=True)

    with col_tag:
        if "tags_clean" in cluster_data.columns:
            tag_df = top_token_frequencies(cluster_data["tags_clean"], top_n=15)
            if not tag_df.empty:
                cluster_name = cluster_names.get(
                    selected_cluster, f"Cluster {selected_cluster}"
                )
                fig_tag = px.bar(
                    tag_df,
                    x="count",
                    y="token",
                    orientation="h",
                    title=f"🏷️ Top Tags in {cluster_name}",
                    color="count",
                    color_continuous_scale="greens",
                    template="plotly_white",
                )
                fig_tag.update_layout(
                    xaxis_title="Frequency",
                    yaxis_title="Tags",
                    height=400,
                    showlegend=False,
                )
                st.plotly_chart(fig_tag, use_container_width=True)

# Display recipe table with modern styling
st.markdown("**Détails des recettes du cluster sélectionné**")
if not cluster_data.empty:
    # Select available columns for display
    display_cols = ["id"]
    col_names = ["ID"]

    # Add name column if available
    if "name" in cluster_data.columns:
        display_cols.append("name")
        col_names.append("Recipe Name")
    elif "description" in cluster_data.columns:
        display_cols.append("description")
        col_names.append("Description")

    # Add metrics
    if "metric_1" in cluster_data.columns:
        display_cols.append("metric_1")
        col_names.append("Metric 1")
    if "metric_2" in cluster_data.columns:
        display_cols.append("metric_2")
        col_names.append("Metric 2")

    # Add time information
    if "minutes" in cluster_data.columns:
        display_cols.append("minutes")
        col_names.append("Minutes")

    # Add ingredients and tags
    if "ingredients_clean" in cluster_data.columns:
        display_cols.append("ingredients_clean")
        col_names.append("Ingredients")
    if "tags_clean" in cluster_data.columns:
        display_cols.append("tags_clean")
        col_names.append("Tags")

    # Create display dataframe
    display_data = cluster_data[display_cols].copy()
    display_data.columns = col_names

    # Create column configuration
    column_config = {}
    for i, col in enumerate(display_cols):
        col_name = col_names[i]
        if col == "id":
            column_config[col_name] = st.column_config.NumberColumn("ID", width="small")
        elif col in ["comp_1", "comp_2"]:
            column_config[col_name] = st.column_config.NumberColumn(
                col_name, format="%.3f", width="small"
            )
        elif col in ["metric_1", "metric_2"]:
            column_config[col_name] = st.column_config.NumberColumn(
                col_name, format="%.2f", width="small"
            )
        elif col == "minutes":
            column_config[col_name] = st.column_config.NumberColumn(
                col_name, format="%.0f", width="small"
            )
        elif col in ["name", "description"]:
            column_config[col_name] = st.column_config.TextColumn(
                col_name, width="medium"
            )
        else:
            column_config[col_name] = st.column_config.TextColumn(
                col_name, width="large"
            )

    # Style the dataframe
    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True,
        column_config=column_config,
    )
else:
    st.warning("No recipes found for the selected cluster.")
