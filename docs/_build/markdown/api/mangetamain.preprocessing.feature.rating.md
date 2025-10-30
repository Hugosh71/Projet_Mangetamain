# mangetamain.preprocessing.feature.rating package

## Submodules

## mangetamain.preprocessing.feature.rating.analyzers module

Analyzers for rating feature.

### *class* mangetamain.preprocessing.feature.rating.analyzers.RatingAnalyser(\*, logger: Logger | None = None)

Bases: [`Analyser`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.Analyser)

Compute per-recipe rating statistics with Bayesian smoothing.

This analyser aggregates interaction ratings by recipe to derive robust
summary statistics. It supports recipes without ratings and uses a simple
empirical Bayes shrinkage toward a global prior to stabilize the mean
rating for recipes with few observations.

Metrics produced include:
- `n_interactions`: total interactions per recipe (rated or not),
- `n_rated` and `share_rated`: count and share of rated interactions,
- `mean_rating`, `median_rating`, `rating_std` over rated-only rows,
- `bayes_mean`: smoothed mean rating with prior strength `c` and

> prior mean `mu` (percentile of the rated distribution).

Optional bounds using the Wilson interval can also be computed for the
proportion of rated interactions per recipe.

#### \_\_init_\_(\*, logger: Logger | None = None) → None

#### analyze(recipes: DataFrame, interactions: DataFrame, \*, c: int | None = None, mu_percentile: float = 0.5, include_zero_ratings: bool = True, with_wilson_per_recipe: bool = False) → [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult)

Aggregate ratings and compute robust per-recipe statistics.

* **Parameters:**
  * **recipes** (*pd.DataFrame*) – Recipe metadata. Only `id` and `name`
    are used (if available) to attach readable labels.
  * **interactions** (*pd.DataFrame*) – Interaction events expected to
    contain:
    - `recipe_id` (int): foreign key to a recipe,
    - `rating` (float or int, optional): rating in [1, 5].
  * **c** (*int* *|* *None*) – Prior strength used in Bayesian mean
    `(mu * c + sum_ratings) / (c + n_rated)`. Defaults to the
    median of `n_rated` or 5, whichever is larger.
  * **mu_percentile** (*float*) – Percentile of the rated-only distribution
    to use as the prior mean `mu`. Default is 0.5 (median).
  * **include_zero_ratings** (*bool*) – Deprecated parameter kept for backward
    compatibility (no effect). Ratings <= 0 are ignored.
  * **with_wilson_per_recipe** (*bool*) – If `True`, compute Wilson bounds
    for `share_rated` per recipe.
* **Returns:**
  Object with
  : - `table`: a DataFrame of per-recipe aggregates and metrics,
    - `summary`: global summary including Wilson bounds over the
      average rated share across recipes.
* **Return type:**
  [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult)
* **Raises:**
  **ValueError** – If `interactions` is missing required columns.

#### generate_report(result: [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult), path: Path) → dict[str, object]

Write CSV outputs for per-recipe metrics and global summary.

The function exports two CSV files in the given directory:
- `rating_table.csv`: per-recipe metrics from [`analyze()`](#mangetamain.preprocessing.feature.rating.analyzers.RatingAnalyser.analyze).
- `rating_summary.csv`: one-row summary table for easy reading.

* **Parameters:**
  * **result** ([*AnalysisResult*](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult)) – Output of [`analyze()`](#mangetamain.preprocessing.feature.rating.analyzers.RatingAnalyser.analyze).
  * **path** (*Path* *|* *str*) – Target directory (or a file whose parent
    directory will be used) where CSVs are written.
* **Returns:**
  Paths of the created files under keys
  : `table_path` and `summary_path`.
* **Return type:**
  dict[str, object]

## mangetamain.preprocessing.feature.rating.strategies module

Strategies specific to rating feature processing.

Implements minimal cleaning and preprocessing hooks for rating interactions.
These can be extended to filter invalid ratings, normalize scales, or enforce
consistency across data sources before analysis.

### *class* mangetamain.preprocessing.feature.rating.strategies.RatingCleaning(\*args, \*\*kwargs)

Bases: [`ICleaningStrategy`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.ICleaningStrategy)

Cleaning strategy for rating interactions.

The current implementation is a no-op placeholder. A production version
could remove ratings outside expected bounds, discard test interactions,
or reconcile duplicates.

#### clean(recipes: DataFrame, interactions: DataFrame) → tuple[DataFrame, DataFrame]

Return cleaned copies of the inputs.

* **Parameters:**
  * **recipes** – Recipes dataframe.
  * **interactions** – Interactions dataframe to be cleaned.
* **Returns:**
  Tuple of possibly transformed `(recipes, interactions)`.

### *class* mangetamain.preprocessing.feature.rating.strategies.RatingPreprocessing(\*args, \*\*kwargs)

Bases: [`IPreprocessingStrategy`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.IPreprocessingStrategy)

Preprocessing strategy for rating interactions.

The current implementation forwards inputs unchanged. A non-trivial
variant may add normalized ratings (e.g., divide by 5) or compute per-user
z-scores to reduce bias.

#### preprocess(recipes: DataFrame, interactions: DataFrame) → tuple[DataFrame, DataFrame]

Return preprocessed copies of the inputs.

* **Parameters:**
  * **recipes** – Recipes dataframe.
  * **interactions** – Interactions dataframe to be preprocessed.
* **Returns:**
  Tuple of possibly transformed `(recipes, interactions)`.

## Module contents

Rating-focused strategies and analyzers.

### *class* mangetamain.preprocessing.feature.rating.RatingCleaning(\*args, \*\*kwargs)

Bases: [`ICleaningStrategy`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.ICleaningStrategy)

Cleaning strategy for rating interactions.

The current implementation is a no-op placeholder. A production version
could remove ratings outside expected bounds, discard test interactions,
or reconcile duplicates.

#### clean(recipes: DataFrame, interactions: DataFrame) → tuple[DataFrame, DataFrame]

Return cleaned copies of the inputs.

* **Parameters:**
  * **recipes** – Recipes dataframe.
  * **interactions** – Interactions dataframe to be cleaned.
* **Returns:**
  Tuple of possibly transformed `(recipes, interactions)`.

### *class* mangetamain.preprocessing.feature.rating.RatingPreprocessing(\*args, \*\*kwargs)

Bases: [`IPreprocessingStrategy`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.IPreprocessingStrategy)

Preprocessing strategy for rating interactions.

The current implementation forwards inputs unchanged. A non-trivial
variant may add normalized ratings (e.g., divide by 5) or compute per-user
z-scores to reduce bias.

#### preprocess(recipes: DataFrame, interactions: DataFrame) → tuple[DataFrame, DataFrame]

Return preprocessed copies of the inputs.

* **Parameters:**
  * **recipes** – Recipes dataframe.
  * **interactions** – Interactions dataframe to be preprocessed.
* **Returns:**
  Tuple of possibly transformed `(recipes, interactions)`.

### *class* mangetamain.preprocessing.feature.rating.RatingAnalyser(\*, logger: Logger | None = None)

Bases: [`Analyser`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.Analyser)

Compute per-recipe rating statistics with Bayesian smoothing.

This analyser aggregates interaction ratings by recipe to derive robust
summary statistics. It supports recipes without ratings and uses a simple
empirical Bayes shrinkage toward a global prior to stabilize the mean
rating for recipes with few observations.

Metrics produced include:
- `n_interactions`: total interactions per recipe (rated or not),
- `n_rated` and `share_rated`: count and share of rated interactions,
- `mean_rating`, `median_rating`, `rating_std` over rated-only rows,
- `bayes_mean`: smoothed mean rating with prior strength `c` and

> prior mean `mu` (percentile of the rated distribution).

Optional bounds using the Wilson interval can also be computed for the
proportion of rated interactions per recipe.

#### \_\_init_\_(\*, logger: Logger | None = None) → None

#### analyze(recipes: DataFrame, interactions: DataFrame, \*, c: int | None = None, mu_percentile: float = 0.5, include_zero_ratings: bool = True, with_wilson_per_recipe: bool = False) → [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult)

Aggregate ratings and compute robust per-recipe statistics.

* **Parameters:**
  * **recipes** (*pd.DataFrame*) – Recipe metadata. Only `id` and `name`
    are used (if available) to attach readable labels.
  * **interactions** (*pd.DataFrame*) – Interaction events expected to
    contain:
    - `recipe_id` (int): foreign key to a recipe,
    - `rating` (float or int, optional): rating in [1, 5].
  * **c** (*int* *|* *None*) – Prior strength used in Bayesian mean
    `(mu * c + sum_ratings) / (c + n_rated)`. Defaults to the
    median of `n_rated` or 5, whichever is larger.
  * **mu_percentile** (*float*) – Percentile of the rated-only distribution
    to use as the prior mean `mu`. Default is 0.5 (median).
  * **include_zero_ratings** (*bool*) – Deprecated parameter kept for backward
    compatibility (no effect). Ratings <= 0 are ignored.
  * **with_wilson_per_recipe** (*bool*) – If `True`, compute Wilson bounds
    for `share_rated` per recipe.
* **Returns:**
  Object with
  : - `table`: a DataFrame of per-recipe aggregates and metrics,
    - `summary`: global summary including Wilson bounds over the
      average rated share across recipes.
* **Return type:**
  [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult)
* **Raises:**
  **ValueError** – If `interactions` is missing required columns.

#### generate_report(result: [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult), path: Path) → dict[str, object]

Write CSV outputs for per-recipe metrics and global summary.

The function exports two CSV files in the given directory:
- `rating_table.csv`: per-recipe metrics from [`analyze()`](#mangetamain.preprocessing.feature.rating.RatingAnalyser.analyze).
- `rating_summary.csv`: one-row summary table for easy reading.

* **Parameters:**
  * **result** ([*AnalysisResult*](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult)) – Output of [`analyze()`](#mangetamain.preprocessing.feature.rating.RatingAnalyser.analyze).
  * **path** (*Path* *|* *str*) – Target directory (or a file whose parent
    directory will be used) where CSVs are written.
* **Returns:**
  Paths of the created files under keys
  : `table_path` and `summary_path`.
* **Return type:**
  dict[str, object]
