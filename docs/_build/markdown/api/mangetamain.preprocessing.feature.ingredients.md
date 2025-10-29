# mangetamain.preprocessing.feature.ingredients package

## Submodules

## mangetamain.preprocessing.feature.ingredients.analysers module

Ingredients analyser module.

### *class* mangetamain.preprocessing.feature.ingredients.analysers.IngredientsAnalyser(cluster_threshold: float | None = None, n_pca_components: int | None = None, embedding_model: str | None = None)

Bases: [`Analyser`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.Analyser)

Analyser that extracts semantic and PCA-based features from recipe ingredients.

This class implements the Analyser interface to process a list of recipes.
It performs two main tasks:
1.  Semantic Analysis: Computes scores for each recipe along predefined

> semantic axes (e.g., sweet vs. savory) using sentence embeddings.
1. Co-occurrence Analysis: Clusters ingredients based on their embeddings,
   builds a co-occurrence matrix, and applies PCA to extract
   principal components as recipe features.

#### cluster_threshold

Distance threshold used for hierarchical clustering of ingredients.

* **Type:**
  float

#### n_pca_components

Number of principal components to compute from the co-occurrence matrix.

* **Type:**
  int

#### embedding_model_name

Name of the SentenceTransformer model used to compute embeddings.

* **Type:**
  str

#### model

The loaded SentenceTransformer model instance.

* **Type:**
  SentenceTransformer

#### DEFAULT_CLUSTER_THRESHOLD *: float* *= 0.5*

#### DEFAULT_N_PCA_COMPONENTS *: int* *= 10*

#### DEFAULT_MODEL_NAME *: str* *= 'all-mpnet-base-v2'*

#### AXES_PHRASES *: dict[str, tuple[str, str]]* *= {'lowcal_rich': ('low-calorie healthy food', 'rich and fatty dish'), 'raw_processed': ('raw natural ingredient', 'processed or prepared food'), 'solid_liquid': ('solid food', 'liquid food or drink'), 'spicy_mild': ('spicy hot food', 'mild gentle flavor'), 'sweet_savory': ('sweet dessert flavor', 'savory meal flavor'), 'vegetarian_meat': ('vegetarian food without meat', 'meat-based dish'), 'western_exotic': ('typical western food', 'exotic or asian food')}*

#### \_\_init_\_(cluster_threshold: float | None = None, n_pca_components: int | None = None, embedding_model: str | None = None) → None

Initialize the IngredientsAnalyser.

* **Parameters:**
  * **cluster_threshold** (*float* *,* *optional*) – The distance threshold for the AgglomerativeClustering.
    If None, defaults to DEFAULT_CLUSTER_THRESHOLD.
  * **n_pca_components** (*int* *,* *optional*) – The number of components for PCA.
    If None, defaults to DEFAULT_N_PCA_COMPONENTS.
  * **embedding_model** (*str* *,* *optional*) – The name of the SentenceTransformer model to load.
    If None, defaults to DEFAULT_MODEL_NAME.

#### analyze(recipes: DataFrame, interactions: DataFrame, \*\*kwargs: object) → [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult)

Main analysis pipeline producing semantic and PCA-based features.

This method executes the full analysis workflow:
1. Extracts ingredients.
2. Computes embeddings.
3. Calculates semantic scores and adds them to recipes.
4. Clusters ingredients.
5. Computes co-occurrence PCA and adds dimensions to recipes.

* **Parameters:**
  * **recipes** (*pd.DataFrame*) – DataFrame containing recipe data, must have an ‘ingredients’ column
    (expected as a string representation of a list).
  * **interactions** (*pd.DataFrame*) – DataFrame of user interactions. (Note: This parameter is part of the
    interface but not used in this specific analyser).
  * **\*\*kwargs** (*object*) – Additional keyword arguments (unused, for interface compatibility).
* **Returns:**
  An object containing a ‘table’ (DataFrame with recipe IDs and
  new features) and a ‘summary’ (dict of mean feature values).
* **Return type:**
  [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult)

#### generate_report(result: [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult), path: str) → dict[str, str]

Stub report generator.

(This is a placeholder and does not generate a real report).

* **Parameters:**
  * **result** ([*AnalysisResult*](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult)) – The result object returned by the analyze method.
  * **path** (*str*) – The file path where the report should be saved.
* **Returns:**
  A dictionary containing paths to the generated report files.
* **Return type:**
  dict[str, str]

## mangetamain.preprocessing.feature.ingredients.strategies module

Ingredients strategies (stubs).

### *class* mangetamain.preprocessing.feature.ingredients.strategies.IngredientsCleaning(\*args, \*\*kwargs)

Bases: [`ICleaningStrategy`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.ICleaningStrategy)

#### clean(recipes: DataFrame, interactions: DataFrame) → tuple[DataFrame, DataFrame]

### *class* mangetamain.preprocessing.feature.ingredients.strategies.IngredientsPreprocessing(\*args, \*\*kwargs)

Bases: [`IPreprocessingStrategy`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.IPreprocessingStrategy)

#### preprocess(recipes: DataFrame, interactions: DataFrame) → tuple[DataFrame, DataFrame]

## Module contents

Ingredients module stubs.

### *class* mangetamain.preprocessing.feature.ingredients.IngredientsCleaning(\*args, \*\*kwargs)

Bases: [`ICleaningStrategy`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.ICleaningStrategy)

#### clean(recipes: DataFrame, interactions: DataFrame) → tuple[DataFrame, DataFrame]

### *class* mangetamain.preprocessing.feature.ingredients.IngredientsPreprocessing(\*args, \*\*kwargs)

Bases: [`IPreprocessingStrategy`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.IPreprocessingStrategy)

#### preprocess(recipes: DataFrame, interactions: DataFrame) → tuple[DataFrame, DataFrame]

### *class* mangetamain.preprocessing.feature.ingredients.IngredientsAnalyser(cluster_threshold: float | None = None, n_pca_components: int | None = None, embedding_model: str | None = None)

Bases: [`Analyser`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.Analyser)

Analyser that extracts semantic and PCA-based features from recipe ingredients.

This class implements the Analyser interface to process a list of recipes.
It performs two main tasks:
1.  Semantic Analysis: Computes scores for each recipe along predefined

> semantic axes (e.g., sweet vs. savory) using sentence embeddings.
1. Co-occurrence Analysis: Clusters ingredients based on their embeddings,
   builds a co-occurrence matrix, and applies PCA to extract
   principal components as recipe features.

#### cluster_threshold

Distance threshold used for hierarchical clustering of ingredients.

* **Type:**
  float

#### n_pca_components

Number of principal components to compute from the co-occurrence matrix.

* **Type:**
  int

#### embedding_model_name

Name of the SentenceTransformer model used to compute embeddings.

* **Type:**
  str

#### model

The loaded SentenceTransformer model instance.

* **Type:**
  SentenceTransformer

#### DEFAULT_CLUSTER_THRESHOLD *: float* *= 0.5*

#### DEFAULT_N_PCA_COMPONENTS *: int* *= 10*

#### DEFAULT_MODEL_NAME *: str* *= 'all-mpnet-base-v2'*

#### AXES_PHRASES *: dict[str, tuple[str, str]]* *= {'lowcal_rich': ('low-calorie healthy food', 'rich and fatty dish'), 'raw_processed': ('raw natural ingredient', 'processed or prepared food'), 'solid_liquid': ('solid food', 'liquid food or drink'), 'spicy_mild': ('spicy hot food', 'mild gentle flavor'), 'sweet_savory': ('sweet dessert flavor', 'savory meal flavor'), 'vegetarian_meat': ('vegetarian food without meat', 'meat-based dish'), 'western_exotic': ('typical western food', 'exotic or asian food')}*

#### \_\_init_\_(cluster_threshold: float | None = None, n_pca_components: int | None = None, embedding_model: str | None = None) → None

Initialize the IngredientsAnalyser.

* **Parameters:**
  * **cluster_threshold** (*float* *,* *optional*) – The distance threshold for the AgglomerativeClustering.
    If None, defaults to DEFAULT_CLUSTER_THRESHOLD.
  * **n_pca_components** (*int* *,* *optional*) – The number of components for PCA.
    If None, defaults to DEFAULT_N_PCA_COMPONENTS.
  * **embedding_model** (*str* *,* *optional*) – The name of the SentenceTransformer model to load.
    If None, defaults to DEFAULT_MODEL_NAME.

#### model *: object | None*

#### analyze(recipes: DataFrame, interactions: DataFrame, \*\*kwargs: object) → [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult)

Main analysis pipeline producing semantic and PCA-based features.

This method executes the full analysis workflow:
1. Extracts ingredients.
2. Computes embeddings.
3. Calculates semantic scores and adds them to recipes.
4. Clusters ingredients.
5. Computes co-occurrence PCA and adds dimensions to recipes.

* **Parameters:**
  * **recipes** (*pd.DataFrame*) – DataFrame containing recipe data, must have an ‘ingredients’ column
    (expected as a string representation of a list).
  * **interactions** (*pd.DataFrame*) – DataFrame of user interactions. (Note: This parameter is part of the
    interface but not used in this specific analyser).
  * **\*\*kwargs** (*object*) – Additional keyword arguments (unused, for interface compatibility).
* **Returns:**
  An object containing a ‘table’ (DataFrame with recipe IDs and
  new features) and a ‘summary’ (dict of mean feature values).
* **Return type:**
  [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult)

#### generate_report(result: [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult), path: str) → dict[str, str]

Stub report generator.

(This is a placeholder and does not generate a real report).

* **Parameters:**
  * **result** ([*AnalysisResult*](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult)) – The result object returned by the analyze method.
  * **path** (*str*) – The file path where the report should be saved.
* **Returns:**
  A dictionary containing paths to the generated report files.
* **Return type:**
  dict[str, str]
