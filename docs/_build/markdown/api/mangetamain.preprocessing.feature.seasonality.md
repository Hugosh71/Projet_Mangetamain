# mangetamain.preprocessing.feature.seasonality package

## Submodules

## mangetamain.preprocessing.feature.seasonality.analyzers module

Seasonality analysers.

This module provides tools to compute and report seasonality features
for recipe interaction data. It extracts cyclic (seasonal) patterns
based on user interactions and represents them as smoothed sine/cosine
features along with a seasonality strength metric.

### *class* mangetamain.preprocessing.feature.seasonality.analyzers.SeasonalityAnalyzer(\*, logger: Logger | None = None)

Bases: [`Analyser`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.Analyser)

Analyzes seasonality patterns in user-recipe interactions.

This analyzer computes seasonality-related features (e.g., sine and cosine
of day-of-year) for each recipe based on user interaction timestamps.
It applies empirical Bayes smoothing to stabilize estimates for recipes
with limited data.

#### \_\_init_\_(\*, logger: Logger | None = None) → None

Initializes the SeasonalityAnalyzer.

* **Parameters:**
  **logger** (*logging.Logger* *|* *None*) – Optional custom logger instance.
  If not provided, a module-level logger will be used.

#### analyze(recipes: DataFrame, interactions: DataFrame, \*\*kwargs: object) → [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult)

Computes seasonality features for recipes based on interaction data.

The method estimates each recipe’s position in the yearly cycle using
the day of year (DOY) of its interactions. It encodes DOY as sine and
cosine features to capture cyclical seasonality and applies empirical
Bayes smoothing to reduce noise in low-sample cases.

* **Parameters:**
  * **recipes** (*pd.DataFrame*) – DataFrame of recipe metadata (unused here but
    required by interface).
  * **interactions** (*pd.DataFrame*) – DataFrame of user interactions containing:
    - ‘recipe_id’: Identifier of the recipe.
    - ‘date’: Date of interaction.
  * **\*\*kwargs** (*object*) – Additional keyword arguments (unused).
* **Returns:**
  Object containing:
  : - table (pd.DataFrame): Per-recipe seasonality features:
      : [‘recipe_id’, ‘inter_doy_sin_smooth’, ‘inter_doy_cos_smooth’, ‘inter_strength’]
    - summary (dict): Empty summary (for compatibility with reporting).
* **Return type:**
  [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult)
* **Raises:**
  **ValueError** – If required columns (‘date’, ‘recipe_id’) are missing
      or if invalid date values are detected.

#### generate_report(result: [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult), path)

Generates and saves CSV reports for seasonality results.

This function saves both a detailed per-recipe feature table and
a summary CSV file in the given directory.

* **Parameters:**
  * **result** ([*AnalysisResult*](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult)) – Result object returned by analyze().
  * **path** (*str* *or* *Path*) – Path to the output directory or file.
    If a directory is provided, files are saved inside it.
    If a file path is given, its parent directory is used.
* **Returns:**
  A dictionary containing:
  : - ’table_path’ (str): Path to the saved per-recipe CSV file.
    - ’summary_path’ (str): Path to the saved summary CSV file.
* **Return type:**
  dict

## mangetamain.preprocessing.feature.seasonality.strategies module

Seasonality strategies (stubs).

Defines the cleaning and preprocessing strategies used by the seasonality
feature processing pipeline. Strategies follow simple interfaces that return
possibly transformed copies of the input `recipes` and `interactions`
dataframes while preserving schema invariants.

### *class* mangetamain.preprocessing.feature.seasonality.strategies.SeasonalityCleaning(\*args, \*\*kwargs)

Bases: [`ICleaningStrategy`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.ICleaningStrategy)

No-op cleaning step for seasonality inputs.

This placeholder keeps the pipeline structure uniform. Implementations may
drop invalid or out-of-range dates, or filter interactions by source.

#### clean(recipes: DataFrame, interactions: DataFrame) → tuple[DataFrame, DataFrame]

Return cleaned copies of the inputs.

* **Parameters:**
  * **recipes** – Recipes dataframe.
  * **interactions** – Interactions dataframe.
* **Returns:**
  Tuple of possibly transformed `(recipes, interactions)`.

### *class* mangetamain.preprocessing.feature.seasonality.strategies.SeasonalityPreprocessing(\*args, \*\*kwargs)

Bases: [`IPreprocessingStrategy`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.IPreprocessingStrategy)

No-op preprocessing step for seasonality inputs.

Real implementations could compute additional intermediate fields such as
normalized timestamps or pre-aggregations used by the analyzer.

#### preprocess(recipes: DataFrame, interactions: DataFrame) → tuple[DataFrame, DataFrame]

Return preprocessed copies of the inputs.

* **Parameters:**
  * **recipes** – Recipes dataframe.
  * **interactions** – Interactions dataframe.
* **Returns:**
  Tuple of possibly transformed `(recipes, interactions)`.

## Module contents

Seasonnality module stubs.

### *class* mangetamain.preprocessing.feature.seasonality.SeasonalityCleaning(\*args, \*\*kwargs)

Bases: [`ICleaningStrategy`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.ICleaningStrategy)

No-op cleaning step for seasonality inputs.

This placeholder keeps the pipeline structure uniform. Implementations may
drop invalid or out-of-range dates, or filter interactions by source.

#### clean(recipes: DataFrame, interactions: DataFrame) → tuple[DataFrame, DataFrame]

Return cleaned copies of the inputs.

* **Parameters:**
  * **recipes** – Recipes dataframe.
  * **interactions** – Interactions dataframe.
* **Returns:**
  Tuple of possibly transformed `(recipes, interactions)`.

### *class* mangetamain.preprocessing.feature.seasonality.SeasonalityPreprocessing(\*args, \*\*kwargs)

Bases: [`IPreprocessingStrategy`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.IPreprocessingStrategy)

No-op preprocessing step for seasonality inputs.

Real implementations could compute additional intermediate fields such as
normalized timestamps or pre-aggregations used by the analyzer.

#### preprocess(recipes: DataFrame, interactions: DataFrame) → tuple[DataFrame, DataFrame]

Return preprocessed copies of the inputs.

* **Parameters:**
  * **recipes** – Recipes dataframe.
  * **interactions** – Interactions dataframe.
* **Returns:**
  Tuple of possibly transformed `(recipes, interactions)`.

### *class* mangetamain.preprocessing.feature.seasonality.SeasonalityAnalyzer(\*, logger: Logger | None = None)

Bases: [`Analyser`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.Analyser)

Analyzes seasonality patterns in user-recipe interactions.

This analyzer computes seasonality-related features (e.g., sine and cosine
of day-of-year) for each recipe based on user interaction timestamps.
It applies empirical Bayes smoothing to stabilize estimates for recipes
with limited data.

#### \_\_init_\_(\*, logger: Logger | None = None) → None

Initializes the SeasonalityAnalyzer.

* **Parameters:**
  **logger** (*logging.Logger* *|* *None*) – Optional custom logger instance.
  If not provided, a module-level logger will be used.

#### analyze(recipes: DataFrame, interactions: DataFrame, \*\*kwargs: object) → [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult)

Computes seasonality features for recipes based on interaction data.

The method estimates each recipe’s position in the yearly cycle using
the day of year (DOY) of its interactions. It encodes DOY as sine and
cosine features to capture cyclical seasonality and applies empirical
Bayes smoothing to reduce noise in low-sample cases.

* **Parameters:**
  * **recipes** (*pd.DataFrame*) – DataFrame of recipe metadata (unused here but
    required by interface).
  * **interactions** (*pd.DataFrame*) – DataFrame of user interactions containing:
    - ‘recipe_id’: Identifier of the recipe.
    - ‘date’: Date of interaction.
  * **\*\*kwargs** (*object*) – Additional keyword arguments (unused).
* **Returns:**
  Object containing:
  : - table (pd.DataFrame): Per-recipe seasonality features:
      : [‘recipe_id’, ‘inter_doy_sin_smooth’, ‘inter_doy_cos_smooth’, ‘inter_strength’]
    - summary (dict): Empty summary (for compatibility with reporting).
* **Return type:**
  [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult)
* **Raises:**
  **ValueError** – If required columns (‘date’, ‘recipe_id’) are missing
      or if invalid date values are detected.

#### generate_report(result: [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult), path)

Generates and saves CSV reports for seasonality results.

This function saves both a detailed per-recipe feature table and
a summary CSV file in the given directory.

* **Parameters:**
  * **result** ([*AnalysisResult*](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult)) – Result object returned by analyze().
  * **path** (*str* *or* *Path*) – Path to the output directory or file.
    If a directory is provided, files are saved inside it.
    If a file path is given, its parent directory is used.
* **Returns:**
  A dictionary containing:
  : - ’table_path’ (str): Path to the saved per-recipe CSV file.
    - ’summary_path’ (str): Path to the saved summary CSV file.
* **Return type:**
  dict
