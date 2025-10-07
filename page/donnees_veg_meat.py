import streamlit as st
import pandas as pd
import plotly.express as px

def show():
    st.title("Mange Ta Main")
    st.title("Bienvenue sur la page d'accueil !")
    st.write("Cliquez sur le brocoli pour accéder aux recettes végétariennes :")

    # Bouton brocoli pour aller aux légumes
    if st.button("🥦 Aller aux recettes végétariennes"):
        st.session_state.page = "vegetables"
    

st.title("Analyse des recettes 🌱🍖")

@st.cache_data
def load_data():
    counts = pd.read_csv("stats_counts.csv")
    means = pd.read_csv("stats_mean.csv")
    ratings = pd.read_csv("stats_rating.csv")
    return counts, means, ratings

# --- Charger les données ---
counts, means, ratings = load_data()

# --- Affichage des données ---
st.subheader("📋 Résumé des données")
st.dataframe(counts)
st.dataframe(means)
st.dataframe(ratings.head())

# --- Barres : moyenne des notes ---
st.subheader("📊 Moyenne des notes par catégorie")
fig_bar = px.bar(means, x="type", y="moyenne_notes", color="type",
                 title="Moyenne des notes (végétarien vs viande)")
st.plotly_chart(fig_bar)

# --- Camembert : proportion des plats ---
st.subheader("🥧 Proportion de plats")
fig_pie = px.pie(counts, names="type", values="nombre", title="Répartition des recettes")
st.plotly_chart(fig_pie)

# --- Histogramme : distribution des notes ---
st.subheader("📉 Distribution des notes")
fig_hist = px.histogram(ratings, x="rating", color="type", nbins=10,
                        title="Distribution des notes selon le type de plat")
st.plotly_chart(fig_hist)



