"""Page d'accueil de l'application"""

import streamlit as st
from pathlib import Path

from src.app.run_all import run_pipeline
from src.app.upload_to_s3 import upload_to_s3_stub
from src.app.download_from_s3 import download_from_s3_stub

st.set_page_config(page_title="Accueil - Mangetamain", page_icon="📈", layout="wide")

st.markdown(
    """
<div style="background-color:#f8f9fa; padding:20px; border-radius:15px;">
<h2 style="text-align:center;">Bienvenue sur Mangetamain !</h2>
<p style="text-align:center;">Explorez nos clusters de recettes bio et traditionnelles 
et découvrez des patterns nutritionnels et sensoriels uniques.</p>
</div>
""",
    unsafe_allow_html=True,
)

st.sidebar.header("🏠 Accueil")

st.write("\n")
st.write("\n")

st.markdown("👋 Bienvenue sur **Mangetamain**!")

st.markdown(
    """
**Mangetamain**, leader de la recommandation B2C de recettes, met à votre disposition 
une application interactive qui vous permet de :  
- Explorer les recettes analysées  
- Visualiser les regroupements (clusters)  
- Découvrir des patterns nutritionnels et sensoriels
"""
)
st.write("\n")
st.write("\n")

st.markdown("### 🔍 Caractéristiques analysées :")

features = [
    ("🍽️", "Densité énergétique"),
    ("🥩", "Proportion protéines/lipides/glucides"),
    ("🥦", "Indice d’équilibre nutritionnel"),
    ("📅", "Dates et interactions"),
    ("⭐", "Nombre d’évaluations"),
    ("📊", "Proportion d’interactions"),
    ("👩‍🍳", "Nombre d’étapes et d’ingrédients"),
    ("⏱️", "Durée de préparation"),
    ("🍭", "Scores sensoriels et nutritionnels"),
]

st.write("\n")


st.write("\n")
cols = st.columns(3)
for i, (emoji, text) in enumerate(features):
    with cols[i % 3]:
        st.markdown(f"{emoji} **{text}**")

st.write("\n")
st.write("\n")

st.markdown(
    """
<div style="background-color:#f8f9fa;padding:15px;border-radius:10px;
text-align:center;">
🚀 Cliquez sur la page 📊 Clustering pour commencer votre exploration des données !
</div>
</div>
""",
    unsafe_allow_html=True,
)

st.write("\n")
st.write("\n")
st.write("\n")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🥗 Recettes analysées", "3 200+")
with col2:
    st.metric("🧩 Clusters identifiés", "5")
with col3:
    st.metric("👩‍🍳 Ingrédients uniques", "1 500+")

st.write("\n")
st.write("\n")

st.markdown("### ⚙️ Pipeline")
btn_run, btn_upload, btn_download = st.columns(3)
with btn_run:
    if st.button("Lancer pipeline", type="primary"):
        try:
            out = run_pipeline()
            st.success(f"Pipeline terminé → {out}")
        except Exception as exc:
            st.error(f"Erreur pipeline: {exc}")
with btn_upload:
    up = st.file_uploader("Uploader CSV local", type=["csv", "gz"])
    if up is not None:
        dest = Path("data/clustering")
        dest.mkdir(parents=True, exist_ok=True)
        target = dest / "recipes_merged.csv.gz"
        with open(target, "wb") as f:
            f.write(up.getbuffer())
        upload_to_s3_stub(target)
        st.success(f"Fichier uploadé vers S3 (stub): {target}")
with btn_download:
    if st.button("Télécharger CSV"):
        local = download_from_s3_stub("recipes_merged.csv.gz")
        st.success(f"Fichier téléchargé (stub): {local}")

st.markdown(
    """
### 🧪 Explorer notre méthodologie
Nous avons construit les clusters à partir d'une analyse regroupant plusieurs 
caractéristiques des recettes, telles que la composition nutritionnelle, les scores 
sensoriels, le nombre d’ingrédients et d’étapes, ainsi que les interactions et 
évaluations des utilisateurs.  

💡 Cliquez sur la page **“Méthodologie”** pour comprendre comment nous avons segmenté 
les recettes et construit nos visualisations.
"""
)
