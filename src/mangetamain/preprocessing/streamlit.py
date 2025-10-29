"""Data preprocessing functions for Streamlit application."""

import ast
import re

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import RobustScaler
from wordcloud import WordCloud

# from .factories import ProcessorFactory
# from .feature.ingredients import IngredientsAnalyser
# from .feature.nutrition import NutritionAnalyser
# from .feature.rating import RatingAnalyser
# from .feature.seasonality import SeasonalityAnalyzer
# from .feature.steps import StepsAnalyser
# from .repositories import CSVDataRepository, RepositoryPaths


# @st.cache_data(persist="disk", show_spinner=False, ttl=None)
# def get_recipes_rating_feature_data() -> pd.DataFrame:
#     repo = CSVDataRepository(paths=RepositoryPaths())
#     processor = ProcessorFactory.create_rating(repo)  # or create_basic
#     processed = processor.run()

#     analyser = RatingAnalyser()
#     result = analyser.analyze(
#         processed.recipes,
#         processed.interactions,
#     )

#     return result.table


# @st.cache_data(persist="disk", show_spinner=False, ttl=None)
# def get_recipes_seasonality_feature_data() -> pd.DataFrame:
#     repo = CSVDataRepository(paths=RepositoryPaths())
#     processor = ProcessorFactory.create_seasonality(repo)
#     processed = processor.run()
#     analyser = SeasonalityAnalyzer()
#     result = analyser.analyze(processed.recipes, processed.interactions)
#     return result.table


# @st.cache_data(persist="disk", show_spinner=False, ttl=None)
# def get_recipes_ingredients_feature_data() -> pd.DataFrame:
#     repo = CSVDataRepository(paths=RepositoryPaths())
#     processor = ProcessorFactory.create_ingredients(repo)
#     processed = processor.run()
#     analyser = IngredientsAnalyser()
#     result = analyser.analyze(processed.recipes, processed.interactions)
#     return result.table


# @st.cache_data(persist="disk", show_spinner=False, ttl=None)
# def get_recipes_nutrition_feature_data() -> pd.DataFrame:
#     repo = CSVDataRepository(paths=RepositoryPaths())
#     processor = ProcessorFactory.create_nutrition(repo)
#     processed = processor.run()
#     analyser = NutritionAnalyser()
#     result = analyser.analyze(processed.recipes, processed.interactions)
#     return result.table


# @st.cache_data(persist="disk", show_spinner=False, ttl=None)
# def get_recipes_steps_feature_data() -> pd.DataFrame:
#     repo = CSVDataRepository(paths=RepositoryPaths())
#     processor = ProcessorFactory.create_steps(repo)
#     processed = processor.run()
#     analyser = StepsAnalyser()
#     result = analyser.analyze(processed.recipes, processed.interactions)
#     return result.table


# @st.cache_data(persist="disk", show_spinner=False, ttl=None)
# def get_recipes_all_feature_data() -> pd.DataFrame:
#     try:
#         combined = pd.concat(
#             [
#                 get_recipes_rating_feature_data(),
#                 get_recipes_seasonality_feature_data(),
#                 get_recipes_ingredients_feature_data(),
#                 get_recipes_nutrition_feature_data(),
#                 get_recipes_steps_feature_data(),
#             ]
#         )
#         return combined, "Concatenated data successfully"
#     except Exception as e:  # keep cached error path informative for UI callers
#         return None, f"Error concatenating data: {e}"


# @st.cache_data(persist="disk", show_spinner=False, ttl=None)
# def save_recipes_all_feature_data(
#     path: Path = Path("data/preprocessed/recipes_all_feature_data.csv"),
# ) -> pd.DataFrame:
#     if not path.parent.exists():
#         path.parent.mkdir(parents=True, exist_ok=True)
#     result = get_recipes_all_feature_data()
#     if isinstance(result, tuple) and len(result) == 2:
#         df, message = result
#     else:
#         df, message = result, "OK"
#     if df is None:
#         return None, message
#     required_cols = [
#         "id",
#         "name",
#         "energy_density",
#         "protein_ratio",
#         "fat_ratio",
#         "nutrient_balance_index",
#         "inter_doy_sin_smooth",
#         "inter_doy_cos_smooth",
#         "inter_strength",
#         "n_interactions",
#         "bayes_mean",
#         "minutes_log",
#         "score_sweet_savory",
#         "score_spicy_mild",
#         "score_lowcal_rich",
#         "score_vegetarian_meat",
#         "score_solid_liquid",
#         "score_raw_processed",
#         "score_western_exotic",
#         "cluster",
#         "pc_1",
#         "pc_2",
#         "tags",
#         "minutes",
#         "n_steps",
#         "n_ingredients",
#         "rating_mean",
#     ]
#     missing = [c for c in required_cols if c not in df.columns]
#     if missing:
#         # raise ValueError(f"Missing required columns: {missing}")
#         # logger = get_logger(__name__)
#         # logger.error(
#         #     f"Missing required columns: {missing}"
#         # )
#         return None, f"Missing required columns: {missing}"
#     df.to_csv(path, index=False)
#     return df, f"Saved data to {path} successfully"


@st.cache_data
def load_recipes_data() -> pd.DataFrame:
    """Load and preprocess recipes data from compressed CSV files.

    Returns:
        pd.DataFrame: Combined recipes and clustering data
    """
    # Load recipes data
    df = None
    target_path = "s3://mangetamain/recipes_merged.csv.gz"
    df = pd.read_csv(target_path)
    if df.empty:
        df = pd.read_csv("data/clustering/recipes_merged.csv.gz")
        if df.empty:
            raise ValueError(f"No data found at {target_path}")

    return df, f"Loaded data from {target_path}"


@st.cache_data
def get_cluster_names() -> dict:
    """Get cluster names mapping.

    Returns:
        dict: Mapping of cluster IDs to names
    """
    return {
        0: "Plats complets équilibrés et élaborés",
        1: "Plats simples et salés",
        2: "Recettes sucrées et riches",
        3: "Snacks sucrés ultra riches",
        4: "Repas rapides semi-équilibrés",
    }


@st.cache_data
def get_col_names(cols=None, return_values=False) -> dict:
    """Get column names mapping.
    Args:
        cols (list, optional): List of column keys to get names for.
        If None, return all.
    Returns:
        dict: Mapping of column keys to French names
    """

    col_map = {
        "id": "ID",
        "name": "Nom de recette",
        "minutes": "Durée de préparation (minutes)",
        "n_steps": "Nombre d'étapes",
        "n_ingredients": "Nombre d'ingrédients",
        "energy_density": "Densité énergétique",
        "protein_ratio": "Proportion de protéines par calorie",
        "fat_ratio": "Proportion de lipides par calorie",
        "nutrient_balance_index": "Indice d'équilibre nutritionnel",
        "score_sweet_savory": "Sucré → Salé",
        "score_spicy_mild": "Épicé → Doux",
        "score_lowcal_rich": "Léger → Riche",
        "score_vegetarian_meat": "Végétarien → Carné",
        "score_solid_liquid": "Solide → Liquide",
        "score_raw_processed": "Cru → Transformé",
        "score_western_exotic": "Occidental → Exotique",
        "rating_mean": "Note moyenne",
    }

    if cols is not None:
        col_names = {col: col_map[col] for col in cols if col in col_map}
    else:
        col_names = col_map

    if return_values:
        return list(col_names.values())
    else:
        return col_names


def remove_outliers_iqr(df, cols, k=5):
    """Remove outliers from specified columns using the IQR method."""
    df_filtered = df.copy()
    for col in cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - k * iqr
        upper = q3 + k * iqr
        df_filtered = df_filtered[
            (df_filtered[col] >= lower) & (df_filtered[col] <= upper)
        ]
    return df_filtered


def add_month_labels(ax):
    """Add French month labels (Jan–Déc) around the unit circle."""
    month_mid_doy = [15, 46, 74, 105, 135, 166, 196, 227, 258, 288, 319, 349]
    month_labels_fr = [
        "Jan",
        "Fév",
        "Mar",
        "Avr",
        "Mai",
        "Jui",
        "Juil",
        "Aoû",
        "Sep",
        "Oct",
        "Nov",
        "Déc",
    ]

    for month, doy in enumerate(month_mid_doy):
        theta = 2 * np.pi * doy / 365
        x = np.cos(theta) * 1.08
        y = np.sin(theta) * 1.08
        ax.text(
            x,
            y,
            month_labels_fr[month],
            ha="center",
            va="center",
            fontsize=9,
            fontweight="bold",
        )


def rgb_to_hex(rgb_str):
    """Convert RGB string to HEX format.
    Args:
        rgb_str: RGB string in the format "rgb(r, g, b)"
    Returns:
        str: HEX color string
    """

    match = re.match(r"rgb\((\d+),\s*(\d+),\s*(\d+)\)", rgb_str)
    if match:
        r, g, b = [int(x) for x in match.groups()]
        return f"#{r:02x}{g:02x}{b:02x}"
    else:
        return rgb_str


def min_max_scale(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    """Apply Min-Max scaling to specified columns in the dataframe.

    Args:
        df: Input dataframe
        cols: List of column names to scale

    Returns:
        pd.DataFrame: DataFrame with scaled columns
    """
    df_scaled = df.copy()
    scaler = RobustScaler()
    df_scaled[cols] = scaler.fit_transform(df[cols])
    return df_scaled


@st.cache_data
def get_tag_cloud(df: pd.DataFrame, tag_col: str, use_tfidf: bool = True):
    """
    Generate a tag cloud using the WordCloud package.

    Args:
        df (pd.DataFrame): DataFrame containing a column with tag lists as
            strings.
        tag_col (str): Column name containing the tags (stringified lists).
        use_tfidf (bool): Whether to compute TF-IDF weights instead of simple
            counts.

    Returns:
        WordCloud: Generated WordCloud object
    """
    # Parse tags column
    df["parsed_tags"] = df[tag_col].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else x
    )

    # Preprocess tags so multi-word tags stay together
    # Replace spaces with underscores: "hello world" → "hello-world"
    df["parsed_tags"] = df["parsed_tags"].apply(
        lambda tags: [
            tag.replace(" ", "-")
            for tag in tags
            if tag not in ["time-to-make", "preparation", "course", "dietary"]
        ]
    )

    # Build corpus (each row = space-separated tags)
    corpus = [" ".join(tags) for tags in df["parsed_tags"]]

    # Compute weights
    if use_tfidf:
        vectorizer = TfidfVectorizer(token_pattern=r"(?u)\b[\w-]+\b")
        X = vectorizer.fit_transform(corpus)
        weights = np.asarray(X.sum(axis=0)).flatten()
        tags = vectorizer.get_feature_names_out()
        tag_weights = dict(zip(tags, weights, strict=False))
    else:
        # Simple count frequency
        all_tags = [tag for tags in df["parsed_tags"] for tag in tags]
        tag_weights = pd.Series(all_tags).value_counts().to_dict()

    # Generate WordCloud
    wordcloud = WordCloud(
        width=300,
        height=300,
        background_color="white",
        colormap="viridis",
        max_words=30,
        random_state=42,
    ).generate_from_frequencies(tag_weights)

    return wordcloud


@st.cache_data
def get_cluster_summary(df: pd.DataFrame, cluster: int):
    df_cluster = df[df["cluster"] == cluster]

    n = df_cluster.shape[0]
    n_steps_mean = df_cluster["n_steps"].mean()
    minutes_mean = df_cluster["minutes"].median()
    n_ingredients = df_cluster["n_ingredients"].mean()

    return {
        "n": n,
        "minutes_mean": minutes_mean,
        "n_steps_mean": n_steps_mean,
        "n_ingredients": n_ingredients,
    }
