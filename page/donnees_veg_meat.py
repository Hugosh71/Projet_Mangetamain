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
    
ratings = pd.read_csv(r"C:\Users\const\TELECOM\DATA\Projet_Mangetamain\data\RAW_interactions.csv")
recipes = pd.read_csv(r"C:\Users\const\TELECOM\DATA\Projet_Mangetamain\data\RAW_recipes.csv")
meat_tags = ["meat", "chicken", "pork", "turkey", "fish", "beef", "lamb"]

data = pd.merge(ratings, recipes, left_on="recipe_id", right_on="id")

print(data.head())

veg = data[data["tags"].str.contains("vegetarian", case=False, na=False)]
meat = data[data["tags"].str.contains("|".join(meat_tags), case=False, na=False)]

# --- Compter et calculer les moyennes ---
nb_veg = len(veg)
nb_meat = len(meat)
moy_veg = veg["rating"].mean()
moy_meat = meat["rating"].mean()

# --- Affichage Streamlit ---
st.title("Analyse des recettes 🌱🍖")

st.write("### Nombre de recettes")
st.write(f"🥦 Végétarien : {nb_veg}")
st.write(f"🍗 Viande : {nb_meat}")

st.write("### Moyenne des notes")
st.write(f"🥦 Végétarien : {moy_veg:.2f}")
st.write(f"🍗 Viande : {moy_meat:.2f}")

# --- Graphiques ---
counts = pd.Series({"Végétarien": nb_veg, "Viande": nb_meat})
means = pd.Series({"Végétarien": moy_veg, "Viande": moy_meat})

# Barres
st.subheader("📊 Moyenne des notes par catégorie")
st.bar_chart(means)

# Camembert
st.subheader("🥧 Répartition des plats")
fig_pie = px.pie(values=counts.values, names=counts.index, title="Proportion de plats")
st.plotly_chart(fig_pie)

# Histogramme
st.subheader("📉 Distribution des notes")
fig_hist = px.histogram(data[data["tags"].str.contains("vegetarian|meat|chicken|pork|fish|beef|lamb", case=False, na=False)],
                        x="rating", color=data["tags"].str.contains("vegetarian", case=False, na=False).map({True: "Végétarien", False: "Viande"}),
                        nbins=10, title="Distribution des notes selon le type de plat")
st.plotly_chart(fig_hist)





