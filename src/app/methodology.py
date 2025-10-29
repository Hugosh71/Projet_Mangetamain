import streamlit as st

st.markdown("""# 🧠 Clustering de Recettes : Méthodologie et Perspectives

Ce document présente la méthodologie utilisée pour construire une **typologie de recettes culinaires** à partir de variables nutritionnelles, sémantiques et comportementales.  
L’objectif est de regrouper les recettes selon leurs similarités globales afin de révéler des familles cohérentes (par exemple : recettes légères et estivales, plats riches et réconfortants, etc.).

---

## 1. 🔍 Variables utilisées pour le clustering

### 1.1. Saison de consommation

**Objectif :** détecter les recettes plutôt **estivales** ou **hivernales**.

**Principe :**
- On observe les **dates de notation** des recettes, supposées corrélées à leur consommation.
- Chaque date est convertie en un **angle en radians** sur un cercle (une année = `2π`).
- On en extrait les **composantes trigonométriques** (`cos` et `sin`), dont on calcule la **moyenne** pour chaque recette.

> 🔹 **Interprétation :**
> - La **direction** du vecteur moyen correspond à la période privilégiée (été, hiver, etc.).
> - La **norme** du vecteur traduit le **degré de saisonnalité** : plus elle est proche de 1, plus la recette est marquée saisonnièrement.

Un **lissage bayésien** (voir encart ci-dessous) a été appliqué afin de réduire les biais pour les recettes ayant très peu de notations.  
Un premier **clustering en trois classes** de saisonnalité a été testé, mais la variable a finalement été **mise de côté** dans cette première version, au profit de variables continues.  
Elle pourra être **intégrée ultérieurement comme variable catégorielle**.

> 📦 **À venir :**
> Une version améliorée du clustering intégrera directement cette typologie saisonnière, jugée plus interprétable.

---

### 1.2. Variables nutritionnelles

Les variables nutritionnelles décrivent le profil énergétique et macroscopique des recettes.

| Variable | Description | Formule simplifiée |
|-----------|--------------|--------------------|
| **Densité énergétique** | Énergie pour 100g | `calories / poids (g)` |
| **Protein ratio** | Part des protéines dans les macronutriments | `protéines / (protéines + lipides + glucides)` |
| **Fat ratio** | Part des lipides dans les macronutriments | `lipides / (protéines + lipides + glucides)` |
| **Nutrient Balance Index (NBI)** | Équilibre global des nutriments | `(protéines - (lipides + sucres + sodium)/3) / (calories + 1)` |

Ces variables permettent de distinguer des profils comme :
- les recettes **hyperprotéinées et légères**,
- les plats **riches et déséquilibrés**,
- ou les recettes **équilibrées et modérées**.

---

### 1.3. Satisfaction moyenne (avec lissage bayésien)

La **note moyenne** des utilisateurs a été ajustée par **lissage bayésien**, afin d’éviter que les recettes peu notées ne soient sur- ou sous-évaluées.

> 🧩 **Encart méthodologique – Le lissage bayésien**
>
> Le lissage bayésien consiste à **pondérer la moyenne empirique** d’un échantillon par une **moyenne globale** :
""")
st.latex(r"""\text{Note corrigée} = \frac{n \times \text{note moyenne recette} 
         + k \times \text{note moyenne globale}}{n + k}""")
st.markdown("""
> où :
> - `n` = nombre de notes de la recette  
> - `k` = poids de la moyenne globale (hyperparamètre)  
>
> Cela permet de réduire la variance pour les petites tailles d’échantillon tout en conservant les différences significatives pour les recettes populaires.

---

### 1.4. Complexité de la recette

Deux dimensions ont été considérées :
- la **durée totale de préparation**,  
- le **nombre d’étapes**.

Ces variables ont été **passées au logarithme** pour réduire la **skewness** (asymétrie) des distributions.  
Une version catégorielle (*simple, moyenne, complexe*) a été explorée via clustering, mais **non utilisée** dans cette première itération.

> 📦 **À venir :**
> Cette variable catégorielle pourrait être exploitée dans une typologie mixte (quantitative + qualitative).

---

### 1.5. Caractérisation sémantique des ingrédients

Chaque ingrédient a été **encodé en embeddings** (modèle `all-mpnet-base-v2`).  
Pour chaque recette, on a ensuite calculé le **cosinus moyen** avec 7 **vecteurs de référence sémantiques** :

| Axe | Interprétation | Pôles |
|------|----------------|-------|
| **Sweet–Savory** | sucré ↔ salé | ("sweet dessert flavor", "savory meal flavor") |
| **Spicy–Mild** | épicé ↔ doux | ("spicy hot food", "mild gentle flavor") |
| **Lowcal–Rich** | léger ↔ riche | ("low-calorie healthy food", "rich and fatty dish") |
| **Vegetarian–Meat** | végétarien ↔ carné | ("vegetarian food without meat", "meat-based dish") |
| **Solid–Liquid** | solide ↔ liquide | ("solid food", "liquid food or drink") |
| **Raw–Processed** | brut ↔ transformé | ("raw natural ingredient", "processed or prepared food") |
| **Western–Exotic** | occidental ↔ exotique | ("typical western food", "exotic or asian food") |

Chaque recette est ainsi décrite par **7 scores moyens**, traduisant son identité gustative et culturelle.

---

## 2. 🧩 Travaux préparatoires et perspectives d’évolution

Un travail parallèle a été mené pour améliorer la **représentation des ingrédients** :
- **Clustering hiérarchique (CAH)** sur les ~40 000 ingrédients, à partir de leur **distance cosinus**, pour regrouper les synonymes, fautes ou variantes lexicales.
- Résultat : environ **1 000 clusters d’ingrédients**, étiquetés par l’ingrédient le plus fréquent.
- Construction d’une **matrice de cooccurrence** : deux ingrédients cooccurrents s’ils apparaissent dans une même recette.
- Réalisation d’une **ACP non normalisée** sur la matrice log-transformée.

> 🎯 **Justification du choix "non normé" :**
> Contrairement à une pondération de type TF-IDF, on souhaite ici **conserver le poids des ingrédients fréquents** (huile, sucre, farine, etc.) : leur fréquence élevée s’accompagne d’une **variance importante**, donc d’un pouvoir discriminant fort.

Les **10 premiers axes** de cette ACP ont été extraits et moyennés par recette, fournissant une représentation **par usage culinaire**, complémentaire à la représentation **sémantique**.

---

## 3. ⚙️ Clustering final

Le **clustering principal** a été réalisé avec un **k-means à distance euclidienne**.  
Le **nombre de classes** a été choisi en fonction de la **stabilité des groupes** et surtout de leur **interprétabilité** qualitative.

---

## 4. ⚠️ Limites et pistes d’amélioration

- Les **corrélations inter-variables** sont globalement faibles, sauf entre variables issues d’un même type (nutrition, sémantique, complexité, etc.).  
  → Cela suggère que les dimensions explorées sont **quasi orthogonales** mais que le signal utile est **dilué**.
- Une **Analyse Factorielle Multiple (AFM)** pourrait permettre de mieux **pondérer les groupes de variables** hétérogènes.
- Une autre voie serait de **clustériser un sous-groupe homogène de variables** (par exemple les ingrédients) puis d’utiliser les autres variables comme **variables descriptives**.

---""")