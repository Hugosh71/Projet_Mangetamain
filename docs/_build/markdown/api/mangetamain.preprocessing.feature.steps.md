# mangetamain.preprocessing.feature.steps package

## Submodules

## mangetamain.preprocessing.feature.steps.analysers module

Steps analysers.

This module provides tools to compute and report recipe complexity
features based on preparation steps, ingredients, and cooking time.
It standardizes recipe attributes, derives categorical complexity
clusters, and produces summary statistics for reporting.

The goal is to quantify recipe complexity in a consistent, scalable way,
useful for recommendation models or descriptive analytics.

### *class* mangetamain.preprocessing.feature.steps.analysers.StepsAnalyser(\*, logger: Logger | None = None)

Bases: [`Analyser`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.Analyser)

Analyzes recipe complexity based on steps, ingredients, and time.

This analyzer computes standardized and categorical representations
of recipe complexity. It standardizes key numeric attributes (e.g.,
number of steps, number of ingredients, preparation time), applies
logarithmic transformation to duration, and groups recipes into
interpretable complexity clusters.

It produces both a per-recipe feature table and a summary report of
global statistics such as mean steps, mean ingredients, and the
correlation between them.

#### \_\_init_\_(\*, logger: Logger | None = None) → None

Initializes the StepsAnalyser.

* **Parameters:**
  **logger** (*logging.Logger* *|* *None*) – Optional custom logger instance.
  If not provided, a module-level logger will be used.

#### analyze(recipes: DataFrame, interactions: DataFrame, \*\*kwargs: object) → [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult)

Computes recipe complexity features based on step and ingredient counts.

The method standardizes numeric columns (minutes, n_steps,
n_ingredients) using z-scores, applies a logarithmic
transformation to minutes, and derives complexity clusters
combining step and ingredient categories. It also computes global
descriptive statistics for reporting.

* **Parameters:**
  * **recipes** (*pd.DataFrame*) – DataFrame containing recipe metadata with
    required columns:
    - `minutes` (float): Total preparation time.
    - `n_steps` (int): Number of procedural steps.
    - `n_ingredients` (int): Number of unique ingredients.
  * **interactions** (*pd.DataFrame*) – Unused placeholder for interface
    compatibility.
  * **\*\*kwargs** (*object*) – Additional keyword arguments (unused).
* **Returns:**
  Object containing:
  : - `table` (pd.DataFrame): Per-recipe complexity features:
      [‘id’, ‘minutes’, ‘n_steps’, ‘n_ingredients’, ‘minutes_z’,
      > ’n_steps_z’, ‘n_ingredients_z’, ‘minutes_log’,
      > ‘cluster_ing_steps’, ‘cluster_label_ing_steps’]
    - `summary` (dict): Aggregated metrics including:
      - ‘moyenne_etapes’
      - ‘moyenne_ingredients’
      - ‘correlation_steps_ingredients’
      - ‘nb_clusters’
* **Return type:**
  [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult)
* **Raises:**
  **ValueError** – If any of the required columns is missing.

#### generate_report(result: [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult), path: Path | str) → dict[str, object]

Generates and saves CSV reports for step-based complexity analysis.

This method exports both a detailed per-recipe complexity table and
a summary of global metrics as separate CSV files.

* **Parameters:**
  * **result** ([*AnalysisResult*](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult)) – Result object returned by [`analyze()`](#mangetamain.preprocessing.feature.steps.analysers.StepsAnalyser.analyze).
  * **path** (*str* *or* *Path*) – Path to output directory or file.
    - If a directory is provided, CSV files are saved inside it.
    - If a file path is given, its parent directory is used.
* **Returns:**
  A dictionary containing:
  : - `table_path` (str): Path to the saved complexity table CSV.
    - `summary_path` (str): Path to the saved summary CSV.
* **Return type:**
  dict

## mangetamain.preprocessing.feature.steps.strategies module

Steps strategies (stubs).

Defines hooks for cleaning and preprocessing time/steps/ingredients metadata
prior to complexity analysis. Extend these strategies to enforce numeric types
and remove impossible values (e.g., negative minutes).

### *class* mangetamain.preprocessing.feature.steps.strategies.StepsCleaning(\*args, \*\*kwargs)

Bases: [`ICleaningStrategy`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.ICleaningStrategy)

No-op cleaning for steps-related fields.

Useful extensions include clipping outliers or imputing missing values.

#### clean(recipes: DataFrame, interactions: DataFrame) → tuple[DataFrame, DataFrame]

Return cleaned copies of the inputs.

* **Parameters:**
  * **recipes** – Recipes dataframe.
  * **interactions** – Interactions dataframe.
* **Returns:**
  Tuple of possibly transformed `(recipes, interactions)`.

### *class* mangetamain.preprocessing.feature.steps.strategies.StepsPreprocessing(\*args, \*\*kwargs)

Bases: [`IPreprocessingStrategy`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.IPreprocessingStrategy)

No-op preprocessing for steps-related fields.

Might compute helper columns used by the analyser.

#### preprocess(recipes: DataFrame, interactions: DataFrame) → tuple[DataFrame, DataFrame]

Return preprocessed copies of the inputs.

* **Parameters:**
  * **recipes** – Recipes dataframe.
  * **interactions** – Interactions dataframe.
* **Returns:**
  Tuple of possibly transformed `(recipes, interactions)`.

## Module contents

Steps module stubs.

### *class* mangetamain.preprocessing.feature.steps.StepsCleaning(\*args, \*\*kwargs)

Bases: [`ICleaningStrategy`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.ICleaningStrategy)

No-op cleaning for steps-related fields.

Useful extensions include clipping outliers or imputing missing values.

#### clean(recipes: DataFrame, interactions: DataFrame) → tuple[DataFrame, DataFrame]

Return cleaned copies of the inputs.

* **Parameters:**
  * **recipes** – Recipes dataframe.
  * **interactions** – Interactions dataframe.
* **Returns:**
  Tuple of possibly transformed `(recipes, interactions)`.

### *class* mangetamain.preprocessing.feature.steps.StepsPreprocessing(\*args, \*\*kwargs)

Bases: [`IPreprocessingStrategy`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.IPreprocessingStrategy)

No-op preprocessing for steps-related fields.

Might compute helper columns used by the analyser.

#### preprocess(recipes: DataFrame, interactions: DataFrame) → tuple[DataFrame, DataFrame]

Return preprocessed copies of the inputs.

* **Parameters:**
  * **recipes** – Recipes dataframe.
  * **interactions** – Interactions dataframe.
* **Returns:**
  Tuple of possibly transformed `(recipes, interactions)`.

### *class* mangetamain.preprocessing.feature.steps.StepsAnalyser(\*, logger: Logger | None = None)

Bases: [`Analyser`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.Analyser)

Analyzes recipe complexity based on steps, ingredients, and time.

This analyzer computes standardized and categorical representations
of recipe complexity. It standardizes key numeric attributes (e.g.,
number of steps, number of ingredients, preparation time), applies
logarithmic transformation to duration, and groups recipes into
interpretable complexity clusters.

It produces both a per-recipe feature table and a summary report of
global statistics such as mean steps, mean ingredients, and the
correlation between them.

#### \_\_init_\_(\*, logger: Logger | None = None) → None

Initializes the StepsAnalyser.

* **Parameters:**
  **logger** (*logging.Logger* *|* *None*) – Optional custom logger instance.
  If not provided, a module-level logger will be used.

#### analyze(recipes: DataFrame, interactions: DataFrame, \*\*kwargs: object) → [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult)

Computes recipe complexity features based on step and ingredient counts.

The method standardizes numeric columns (minutes, n_steps,
n_ingredients) using z-scores, applies a logarithmic
transformation to minutes, and derives complexity clusters
combining step and ingredient categories. It also computes global
descriptive statistics for reporting.

* **Parameters:**
  * **recipes** (*pd.DataFrame*) – DataFrame containing recipe metadata with
    required columns:
    - `minutes` (float): Total preparation time.
    - `n_steps` (int): Number of procedural steps.
    - `n_ingredients` (int): Number of unique ingredients.
  * **interactions** (*pd.DataFrame*) – Unused placeholder for interface
    compatibility.
  * **\*\*kwargs** (*object*) – Additional keyword arguments (unused).
* **Returns:**
  Object containing:
  : - `table` (pd.DataFrame): Per-recipe complexity features:
      [‘id’, ‘minutes’, ‘n_steps’, ‘n_ingredients’, ‘minutes_z’,
      > ’n_steps_z’, ‘n_ingredients_z’, ‘minutes_log’,
      > ‘cluster_ing_steps’, ‘cluster_label_ing_steps’]
    - `summary` (dict): Aggregated metrics including:
      - ‘moyenne_etapes’
      - ‘moyenne_ingredients’
      - ‘correlation_steps_ingredients’
      - ‘nb_clusters’
* **Return type:**
  [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult)
* **Raises:**
  **ValueError** – If any of the required columns is missing.

#### generate_report(result: [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult), path: Path | str) → dict[str, object]

Generates and saves CSV reports for step-based complexity analysis.

This method exports both a detailed per-recipe complexity table and
a summary of global metrics as separate CSV files.

* **Parameters:**
  * **result** ([*AnalysisResult*](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult)) – Result object returned by [`analyze()`](#mangetamain.preprocessing.feature.steps.StepsAnalyser.analyze).
  * **path** (*str* *or* *Path*) – Path to output directory or file.
    - If a directory is provided, CSV files are saved inside it.
    - If a file path is given, its parent directory is used.
* **Returns:**
  A dictionary containing:
  : - `table_path` (str): Path to the saved complexity table CSV.
    - `summary_path` (str): Path to the saved summary CSV.
* **Return type:**
  dict
