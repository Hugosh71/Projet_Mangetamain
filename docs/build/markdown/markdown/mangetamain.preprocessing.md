# mangetamain.preprocessing package

## Subpackages

* [mangetamain.preprocessing.feature package](mangetamain.preprocessing.feature.md)
  * [Subpackages](mangetamain.preprocessing.feature.md#subpackages)
    * [mangetamain.preprocessing.feature.ingredients package](mangetamain.preprocessing.feature.ingredients.md)
      * [Submodules](mangetamain.preprocessing.feature.ingredients.md#submodules)
      * [mangetamain.preprocessing.feature.ingredients.analysers module](mangetamain.preprocessing.feature.ingredients.md#module-mangetamain.preprocessing.feature.ingredients.analysers)
      * [mangetamain.preprocessing.feature.ingredients.strategies module](mangetamain.preprocessing.feature.ingredients.md#module-mangetamain.preprocessing.feature.ingredients.strategies)
    * [mangetamain.preprocessing.feature.nutrition package](mangetamain.preprocessing.feature.nutrition.md)
      * [Submodules](mangetamain.preprocessing.feature.nutrition.md#submodules)
      * [mangetamain.preprocessing.feature.nutrition.analysers module](mangetamain.preprocessing.feature.nutrition.md#module-mangetamain.preprocessing.feature.nutrition.analysers)
      * [mangetamain.preprocessing.feature.nutrition.strategies module](mangetamain.preprocessing.feature.nutrition.md#module-mangetamain.preprocessing.feature.nutrition.strategies)
    * [mangetamain.preprocessing.feature.rating package](mangetamain.preprocessing.feature.rating.md)
      * [Submodules](mangetamain.preprocessing.feature.rating.md#submodules)
      * [mangetamain.preprocessing.feature.rating.analyzers module](mangetamain.preprocessing.feature.rating.md#module-mangetamain.preprocessing.feature.rating.analyzers)
      * [mangetamain.preprocessing.feature.rating.strategies module](mangetamain.preprocessing.feature.rating.md#module-mangetamain.preprocessing.feature.rating.strategies)
    * [mangetamain.preprocessing.feature.seasonality package](mangetamain.preprocessing.feature.seasonality.md)
      * [Submodules](mangetamain.preprocessing.feature.seasonality.md#submodules)
      * [mangetamain.preprocessing.feature.seasonality.analyzers module](mangetamain.preprocessing.feature.seasonality.md#module-mangetamain.preprocessing.feature.seasonality.analyzers)
      * [mangetamain.preprocessing.feature.seasonality.strategies module](mangetamain.preprocessing.feature.seasonality.md#module-mangetamain.preprocessing.feature.seasonality.strategies)
    * [mangetamain.preprocessing.feature.steps package](mangetamain.preprocessing.feature.steps.md)
      * [Submodules](mangetamain.preprocessing.feature.steps.md#submodules)
      * [mangetamain.preprocessing.feature.steps.analysers module](mangetamain.preprocessing.feature.steps.md#module-mangetamain.preprocessing.feature.steps.analysers)
      * [mangetamain.preprocessing.feature.steps.strategies module](mangetamain.preprocessing.feature.steps.md#module-mangetamain.preprocessing.feature.steps.strategies)
  * [Module contents](mangetamain.preprocessing.feature.md#module-mangetamain.preprocessing.feature)

## Submodules

## mangetamain.preprocessing.exceptions module

Custom exceptions for backend operations.

### *exception* mangetamain.preprocessing.exceptions.DataError

Bases: `RuntimeError`

Base error for data related failures.

### *exception* mangetamain.preprocessing.exceptions.DataNotFoundError

Bases: [`DataError`](#mangetamain.preprocessing.exceptions.DataError)

Raised when an expected file or resource cannot be located.

### *exception* mangetamain.preprocessing.exceptions.DataLoadError

Bases: [`DataError`](#mangetamain.preprocessing.exceptions.DataError)

Raised when loading data fails due to format or IO errors.

### *exception* mangetamain.preprocessing.exceptions.ValidationError

Bases: [`DataError`](#mangetamain.preprocessing.exceptions.DataError)

Raised when data validation fails.

## mangetamain.preprocessing.factories module

Factories to assemble backend components with sensible defaults.

### *class* mangetamain.preprocessing.factories.ProcessorFactory

Bases: `object`

Build preconfigured processors with default strategies.

#### *static* create_basic(repository, \*, logger: Logger | None = None) → [BasicDataProcessor](#mangetamain.preprocessing.processors.BasicDataProcessor)

#### *static* create_rating(repository, \*, logger: Logger | None = None) → [BasicDataProcessor](#mangetamain.preprocessing.processors.BasicDataProcessor)

#### *static* create_seasonality(repository, \*, logger: Logger | None = None) → [BasicDataProcessor](#mangetamain.preprocessing.processors.BasicDataProcessor)

#### *static* create_ingredients(repository, \*, logger: Logger | None = None) → [BasicDataProcessor](#mangetamain.preprocessing.processors.BasicDataProcessor)

#### *static* create_nutrition(repository, \*, logger: Logger | None = None) → [BasicDataProcessor](#mangetamain.preprocessing.processors.BasicDataProcessor)

#### *static* create_steps(repository, \*, logger: Logger | None = None) → [BasicDataProcessor](#mangetamain.preprocessing.processors.BasicDataProcessor)

## mangetamain.preprocessing.feature_engineering module

### *class* mangetamain.preprocessing.feature_engineering.RecipeSeasonalityFeatureBuilder(date_col='date', group_col='recipe_id', k=5.0)

Bases: `BaseEstimator`, `TransformerMixin`

Transformer that computes seasonality features for recipes based on user
interaction data.

#### \_\_init_\_(date_col='date', group_col='recipe_id', k=5.0)

* **Parameters:**
  * **date_col** (*str*) – Name of the date column in the interactions DataFrame.
  * **group_col** (*str*) – Name of the column used to group interactions (e.g., recipe_id).
  * **k** (*float*) – Empirical Bayes smoothing strength. Higher values apply stronger shrinkage
    toward the global seasonal mean.

#### fit(X: DataFrame, y=None)

Learn seasonal interaction patterns from the interactions table.

* **Parameters:**
  * **X** (*pd.DataFrame*) – Interaction table containing at least date_col and group_col.
  * **y** (*ignored*) – Not used (exists for sklearn compatibility).
* **Returns:**
  **self** – Fitted transformer.
* **Return type:**
  object

#### transform(X: DataFrame)

Merge the precomputed seasonality features into the recipes DataFrame.

* **Parameters:**
  **X** (*pd.DataFrame*) – Recipes table containing group_col (e.g., recipe_id).
* **Returns:**
  **X_out** – Recipes table with added seasonality feature columns.
* **Return type:**
  pd.DataFrame

## mangetamain.preprocessing.interfaces module

Abstract interfaces and strategies for backend processing.

### *class* mangetamain.preprocessing.interfaces.IDataRepository

Bases: `ABC`

Abstraction for loading raw dataframes from a data source.

#### *abstract* load_recipes() → DataFrame

Return the raw recipes dataframe.

#### *abstract* load_interactions() → DataFrame

Return the raw interactions dataframe.

### *class* mangetamain.preprocessing.interfaces.IValidator

Bases: `ABC`

Validation contract applied to dataframes before processing.

#### *abstract* validate(df: DataFrame) → None

Raise on invalid dataframe; return None on success.

### *class* mangetamain.preprocessing.interfaces.ICleaningStrategy(\*args, \*\*kwargs)

Bases: `Protocol`

Strategy to clean raw dataframes prior to preprocessing.

#### clean(recipes: DataFrame, interactions: DataFrame) → tuple[DataFrame, DataFrame]

#### \_\_init_\_(\*args, \*\*kwargs)

### *class* mangetamain.preprocessing.interfaces.IPreprocessingStrategy(\*args, \*\*kwargs)

Bases: `Protocol`

Strategy to transform cleaned dataframes into model-ready form.

#### preprocess(recipes: DataFrame, interactions: DataFrame) → tuple[DataFrame, DataFrame]

#### \_\_init_\_(\*args, \*\*kwargs)

### *class* mangetamain.preprocessing.interfaces.ProcessedPair(recipes: DataFrame, interactions: DataFrame)

Bases: `object`

Container for a pair of dataframes used across the pipeline.

#### recipes *: DataFrame*

#### interactions *: DataFrame*

#### \_\_init_\_(recipes: DataFrame, interactions: DataFrame) → None

### *class* mangetamain.preprocessing.interfaces.AnalysisResult(table: DataFrame, summary: dict[str, object])

Bases: `object`

Container for analyzer outputs shared across implementations.

#### table *: DataFrame*

#### summary *: dict[str, object]*

#### \_\_init_\_(table: DataFrame, summary: dict[str, object]) → None

### *class* mangetamain.preprocessing.interfaces.Analyser

Bases: `ABC`

Abstract base for domain analyzers (rating, ingredients, steps, …).

#### *abstract* analyze(recipes: DataFrame, interactions: DataFrame, \*\*kwargs: object) → [AnalysisResult](#mangetamain.preprocessing.interfaces.AnalysisResult)

Produce analysis artefacts from processed dataframes.

#### *abstract* generate_report(result: [AnalysisResult](#mangetamain.preprocessing.interfaces.AnalysisResult), path: Path) → dict[str, object]

Return a minimal, serializable representation of the result.

### *class* mangetamain.preprocessing.interfaces.DataProcessor(repository: [IDataRepository](#mangetamain.preprocessing.interfaces.IDataRepository), \*, logger: Logger | None = None)

Bases: `ABC`

Abstract processor defining the high-level pipeline steps.

Subclasses typically orchestrate a repository and strategies to
implement `clean` and `preprocess` while exposing a `run` helper.

#### \_\_init_\_(repository: [IDataRepository](#mangetamain.preprocessing.interfaces.IDataRepository), \*, logger: Logger | None = None) → None

#### *abstract* clean(recipes: DataFrame, interactions: DataFrame) → [ProcessedPair](#mangetamain.preprocessing.interfaces.ProcessedPair)

Return cleaned dataframes.

#### *abstract* preprocess(recipes: DataFrame, interactions: DataFrame) → [ProcessedPair](#mangetamain.preprocessing.interfaces.ProcessedPair)

Return preprocessed dataframes.

#### run() → [ProcessedPair](#mangetamain.preprocessing.interfaces.ProcessedPair)

Load, clean, and preprocess data in sequence.

## mangetamain.preprocessing.processors module

Concrete data processors and default strategies.

### *class* mangetamain.preprocessing.processors.NoOpCleaning(\*args, \*\*kwargs)

Bases: [`ICleaningStrategy`](#mangetamain.preprocessing.interfaces.ICleaningStrategy)

No-op cleaning strategy to keep processors generic by default.

#### clean(recipes: DataFrame, interactions: DataFrame) → tuple[DataFrame, DataFrame]

### *class* mangetamain.preprocessing.processors.NoOpPreprocessing(\*args, \*\*kwargs)

Bases: [`IPreprocessingStrategy`](#mangetamain.preprocessing.interfaces.IPreprocessingStrategy)

No-op preprocessing strategy.

#### preprocess(recipes: DataFrame, interactions: DataFrame) → tuple[DataFrame, DataFrame]

### *class* mangetamain.preprocessing.processors.BasicDataProcessor(repository, \*, cleaning: [ICleaningStrategy](#mangetamain.preprocessing.interfaces.ICleaningStrategy) | None = None, preprocessing: [IPreprocessingStrategy](#mangetamain.preprocessing.interfaces.IPreprocessingStrategy) | None = None, logger: Logger | None = None)

Bases: [`DataProcessor`](#mangetamain.preprocessing.interfaces.DataProcessor)

Orchestrates cleaning and preprocessing via Strategy pattern.

#### \_\_init_\_(repository, \*, cleaning: [ICleaningStrategy](#mangetamain.preprocessing.interfaces.ICleaningStrategy) | None = None, preprocessing: [IPreprocessingStrategy](#mangetamain.preprocessing.interfaces.IPreprocessingStrategy) | None = None, logger: Logger | None = None) → None

#### clean(recipes: DataFrame, interactions: DataFrame) → [ProcessedPair](#mangetamain.preprocessing.interfaces.ProcessedPair)

Return cleaned dataframes.

#### preprocess(recipes: DataFrame, interactions: DataFrame) → [ProcessedPair](#mangetamain.preprocessing.interfaces.ProcessedPair)

Return preprocessed dataframes.

## mangetamain.preprocessing.repositories module

Repository implementations for loading raw data.

### *class* mangetamain.preprocessing.repositories.RepositoryPaths(recipes_csv: str = 'data/RAW_recipes.csv', interactions_csv: str = 'data/RAW_interactions.csv')

Bases: `object`

Filesystem locations for raw CSV inputs.

#### recipes_csv *: str* *= 'data/RAW_recipes.csv'*

#### interactions_csv *: str* *= 'data/RAW_interactions.csv'*

#### \_\_init_\_(recipes_csv: str = 'data/RAW_recipes.csv', interactions_csv: str = 'data/RAW_interactions.csv') → None

### *class* mangetamain.preprocessing.repositories.CSVDataRepository(paths: [RepositoryPaths](#mangetamain.preprocessing.repositories.RepositoryPaths) | None = None, \*, recipe_usecols: Sequence[str] | None = None, interaction_usecols: Sequence[str] | None = None, logger: Logger | None = None)

Bases: [`IDataRepository`](#mangetamain.preprocessing.interfaces.IDataRepository)

Load dataframes from CSV files with optional column selection.

#### \_\_init_\_(paths: [RepositoryPaths](#mangetamain.preprocessing.repositories.RepositoryPaths) | None = None, \*, recipe_usecols: Sequence[str] | None = None, interaction_usecols: Sequence[str] | None = None, logger: Logger | None = None) → None

#### load_recipes() → DataFrame

Return the raw recipes dataframe.

#### load_interactions() → DataFrame

Return the raw interactions dataframe.

## mangetamain.preprocessing.streamlit module

Data preprocessing functions for Streamlit application.

### mangetamain.preprocessing.streamlit.load_recipes_data() → DataFrame

Load and preprocess recipes data from compressed CSV files.

* **Returns:**
  Combined recipes and clustering data
* **Return type:**
  pd.DataFrame

### mangetamain.preprocessing.streamlit.get_cluster_names() → dict

Get cluster names mapping.

* **Returns:**
  Mapping of cluster IDs to names
* **Return type:**
  dict

### mangetamain.preprocessing.streamlit.get_col_names(cols=None, return_values=False) → dict

Get column names mapping.
:param cols: List of column keys to get names for.
:type cols: list, optional
:param If None:
:param return all.:

* **Returns:**
  Mapping of column keys to French names
* **Return type:**
  dict

### mangetamain.preprocessing.streamlit.remove_outliers_iqr(df, cols, k=5)

Remove outliers from specified columns using the IQR method.

### mangetamain.preprocessing.streamlit.add_month_labels(ax)

Add French month labels (Jan–Déc) around the unit circle.

### mangetamain.preprocessing.streamlit.rgb_to_hex(rgb_str)

Convert RGB string to HEX format.
:param rgb_str: RGB string in the format “rgb(r, g, b)”

* **Returns:**
  HEX color string
* **Return type:**
  str

### mangetamain.preprocessing.streamlit.min_max_scale(df: DataFrame, cols: list) → DataFrame

Apply Min-Max scaling to specified columns in the dataframe.

* **Parameters:**
  * **df** – Input dataframe
  * **cols** – List of column names to scale
* **Returns:**
  DataFrame with scaled columns
* **Return type:**
  pd.DataFrame

### mangetamain.preprocessing.streamlit.get_tag_cloud(df: DataFrame, tag_col: str, use_tfidf: bool = True)

Generate a tag cloud using the WordCloud package.

* **Parameters:**
  * **df** (*pd.DataFrame*) – DataFrame containing a column with tag lists as
    strings.
  * **tag_col** (*str*) – Column name containing the tags (stringified lists).
  * **use_tfidf** (*bool*) – Whether to compute TF-IDF weights instead of simple
    counts.
* **Returns:**
  Generated WordCloud object
* **Return type:**
  WordCloud

### mangetamain.preprocessing.streamlit.get_cluster_summary(df: DataFrame, cluster: int)

Compute summary statistics for a specific cluster in the recipes DataFrame.

* **Parameters:**
  * **df** (*pd.DataFrame*) – DataFrame containing recipe data with a “cluster” column.
  * **cluster** (*int*) – Cluster ID for which summary statistics are computed.
* **Returns:**
  Dictionary with summary statistics including:
  : - ”n”: Number of recipes in the cluster
    - ”minutes_mean”: Median preparation time (in minutes) for the cluster
    - ”n_steps_mean”: Mean number of steps for the cluster
    - ”n_ingredients”: Mean number of ingredients for the cluster
* **Return type:**
  dict

## Module contents

Backend OOP primitives for Mangetamain.

This package contains abstract interfaces, concrete implementations,
and utilities for data access, preprocessing, and analysis following
SOLID principles and reusable design patterns (Factory, Strategy).

### *class* mangetamain.preprocessing.IDataRepository

Bases: `ABC`

Abstraction for loading raw dataframes from a data source.

#### *abstract* load_recipes() → DataFrame

Return the raw recipes dataframe.

#### *abstract* load_interactions() → DataFrame

Return the raw interactions dataframe.

### *class* mangetamain.preprocessing.IValidator

Bases: `ABC`

Validation contract applied to dataframes before processing.

#### *abstract* validate(df: DataFrame) → None

Raise on invalid dataframe; return None on success.

### *class* mangetamain.preprocessing.DataProcessor(repository: [IDataRepository](#mangetamain.preprocessing.interfaces.IDataRepository), \*, logger: Logger | None = None)

Bases: `ABC`

Abstract processor defining the high-level pipeline steps.

Subclasses typically orchestrate a repository and strategies to
implement `clean` and `preprocess` while exposing a `run` helper.

#### \_\_init_\_(repository: [IDataRepository](#mangetamain.preprocessing.interfaces.IDataRepository), \*, logger: Logger | None = None) → None

#### *abstract* clean(recipes: DataFrame, interactions: DataFrame) → [ProcessedPair](#mangetamain.preprocessing.interfaces.ProcessedPair)

Return cleaned dataframes.

#### *abstract* preprocess(recipes: DataFrame, interactions: DataFrame) → [ProcessedPair](#mangetamain.preprocessing.interfaces.ProcessedPair)

Return preprocessed dataframes.

#### run() → [ProcessedPair](#mangetamain.preprocessing.interfaces.ProcessedPair)

Load, clean, and preprocess data in sequence.

### *class* mangetamain.preprocessing.Analyser

Bases: `ABC`

Abstract base for domain analyzers (rating, ingredients, steps, …).

#### *abstract* analyze(recipes: DataFrame, interactions: DataFrame, \*\*kwargs: object) → [AnalysisResult](#mangetamain.preprocessing.interfaces.AnalysisResult)

Produce analysis artefacts from processed dataframes.

#### *abstract* generate_report(result: [AnalysisResult](#mangetamain.preprocessing.interfaces.AnalysisResult), path: Path) → dict[str, object]

Return a minimal, serializable representation of the result.

### *class* mangetamain.preprocessing.AnalysisResult(table: DataFrame, summary: dict[str, object])

Bases: `object`

Container for analyzer outputs shared across implementations.

#### table *: DataFrame*

#### summary *: dict[str, object]*

#### \_\_init_\_(table: DataFrame, summary: dict[str, object]) → None

### *class* mangetamain.preprocessing.ICleaningStrategy(\*args, \*\*kwargs)

Bases: `Protocol`

Strategy to clean raw dataframes prior to preprocessing.

#### clean(recipes: DataFrame, interactions: DataFrame) → tuple[DataFrame, DataFrame]

#### \_\_init_\_(\*args, \*\*kwargs)

### *class* mangetamain.preprocessing.IPreprocessingStrategy(\*args, \*\*kwargs)

Bases: `Protocol`

Strategy to transform cleaned dataframes into model-ready form.

#### preprocess(recipes: DataFrame, interactions: DataFrame) → tuple[DataFrame, DataFrame]

#### \_\_init_\_(\*args, \*\*kwargs)

### *exception* mangetamain.preprocessing.DataError

Bases: `RuntimeError`

Base error for data related failures.

### *exception* mangetamain.preprocessing.DataNotFoundError

Bases: [`DataError`](#mangetamain.preprocessing.exceptions.DataError)

Raised when an expected file or resource cannot be located.

### *exception* mangetamain.preprocessing.DataLoadError

Bases: [`DataError`](#mangetamain.preprocessing.exceptions.DataError)

Raised when loading data fails due to format or IO errors.

### *exception* mangetamain.preprocessing.ValidationError

Bases: [`DataError`](#mangetamain.preprocessing.exceptions.DataError)

Raised when data validation fails.

### *class* mangetamain.preprocessing.RepositoryPaths(recipes_csv: str = 'data/RAW_recipes.csv', interactions_csv: str = 'data/RAW_interactions.csv')

Bases: `object`

Filesystem locations for raw CSV inputs.

#### recipes_csv *: str* *= 'data/RAW_recipes.csv'*

#### interactions_csv *: str* *= 'data/RAW_interactions.csv'*

#### \_\_init_\_(recipes_csv: str = 'data/RAW_recipes.csv', interactions_csv: str = 'data/RAW_interactions.csv') → None

### *class* mangetamain.preprocessing.CSVDataRepository(paths: [RepositoryPaths](#mangetamain.preprocessing.repositories.RepositoryPaths) | None = None, \*, recipe_usecols: Sequence[str] | None = None, interaction_usecols: Sequence[str] | None = None, logger: Logger | None = None)

Bases: [`IDataRepository`](#mangetamain.preprocessing.interfaces.IDataRepository)

Load dataframes from CSV files with optional column selection.

#### \_\_init_\_(paths: [RepositoryPaths](#mangetamain.preprocessing.repositories.RepositoryPaths) | None = None, \*, recipe_usecols: Sequence[str] | None = None, interaction_usecols: Sequence[str] | None = None, logger: Logger | None = None) → None

#### load_recipes() → DataFrame

Return the raw recipes dataframe.

#### load_interactions() → DataFrame

Return the raw interactions dataframe.

### *class* mangetamain.preprocessing.BasicDataProcessor(repository, \*, cleaning: [ICleaningStrategy](#mangetamain.preprocessing.interfaces.ICleaningStrategy) | None = None, preprocessing: [IPreprocessingStrategy](#mangetamain.preprocessing.interfaces.IPreprocessingStrategy) | None = None, logger: Logger | None = None)

Bases: [`DataProcessor`](#mangetamain.preprocessing.interfaces.DataProcessor)

Orchestrates cleaning and preprocessing via Strategy pattern.

#### \_\_init_\_(repository, \*, cleaning: [ICleaningStrategy](#mangetamain.preprocessing.interfaces.ICleaningStrategy) | None = None, preprocessing: [IPreprocessingStrategy](#mangetamain.preprocessing.interfaces.IPreprocessingStrategy) | None = None, logger: Logger | None = None) → None

#### clean(recipes: DataFrame, interactions: DataFrame) → [ProcessedPair](#mangetamain.preprocessing.interfaces.ProcessedPair)

Return cleaned dataframes.

#### preprocess(recipes: DataFrame, interactions: DataFrame) → [ProcessedPair](#mangetamain.preprocessing.interfaces.ProcessedPair)

Return preprocessed dataframes.

### *class* mangetamain.preprocessing.ProcessorFactory

Bases: `object`

Build preconfigured processors with default strategies.

#### *static* create_basic(repository, \*, logger: Logger | None = None) → [BasicDataProcessor](#mangetamain.preprocessing.processors.BasicDataProcessor)

#### *static* create_rating(repository, \*, logger: Logger | None = None) → [BasicDataProcessor](#mangetamain.preprocessing.processors.BasicDataProcessor)

#### *static* create_seasonality(repository, \*, logger: Logger | None = None) → [BasicDataProcessor](#mangetamain.preprocessing.processors.BasicDataProcessor)

#### *static* create_ingredients(repository, \*, logger: Logger | None = None) → [BasicDataProcessor](#mangetamain.preprocessing.processors.BasicDataProcessor)

#### *static* create_nutrition(repository, \*, logger: Logger | None = None) → [BasicDataProcessor](#mangetamain.preprocessing.processors.BasicDataProcessor)

#### *static* create_steps(repository, \*, logger: Logger | None = None) → [BasicDataProcessor](#mangetamain.preprocessing.processors.BasicDataProcessor)
