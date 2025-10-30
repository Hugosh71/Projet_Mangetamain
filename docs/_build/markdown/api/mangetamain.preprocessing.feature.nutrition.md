# mangetamain.preprocessing.feature.nutrition package

## Submodules

## mangetamain.preprocessing.feature.nutrition.analysers module

Nutrition analyser module.

This module defines the NutritionAnalyser\`class, which extracts and computes
nutritional-based features from recipe metadata (calories, fat, sugar, protein, etc.).
It follows the Analyser interface and produces an AnalysisResult object
containing a feature table and summary statistics.

### *class* mangetamain.preprocessing.feature.nutrition.analysers.NutritionAnalyser

Bases: [`Analyser`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.Analyser)

Analyser computing nutrition-based features from recipe metadata.

This analyser extracts structured nutritional data (e.g., calories, fat,
protein, sugar) from the “nutrition” field of the recipes DataFrame.
It computes several derived indicators useful for downstream modeling
or recommendation tasks, such as energy density and nutrient balance.

### None explicitly defined — this class is stateless.

#### analyze(recipes: DataFrame, interactions: DataFrame | None = None, \*\*kwargs: object) → [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult)

Compute nutrition-based features for each recipe.

This method parses the “nutrition” field of the recipes DataFrame,
extracts individual nutrient values, and derives higher-level
indicators summarizing the nutritional composition of each recipe.

The computed features include:
- **energy_density**: ratio of calories to total macronutrients (fat + carbs + protein).
- **protein_ratio**: fraction of calories contributed by proteins.
- **fat_ratio**: fraction of calories contributed by fats.
- **nutrient_balance_index**: heuristic index combining protein and negative nutrients

> (fat, sugar, sodium) normalized by total calories.
* **Parameters:**
  * **recipes** (*pd.DataFrame*) – DataFrame containing recipe metadata.
    Must include a “nutrition” column, typically a stringified list such as:
    “[calories, fat, sugar, sodium, protein, sat_fat, carbs]”.
  * **interactions** (*pd.DataFrame* *,* *optional*) – DataFrame of user interactions (unused in this analyser, kept for interface compatibility).
  * **\*\*kwargs** (*object*) – Additional arguments passed for interface consistency (ignored).
* **Returns:**
  Object containing:
  - **table**: a DataFrame with one row per recipe and the computed nutrition features.
  - **summary**: a dictionary of global mean values and recipe count.
* **Return type:**
  [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult)
* **Raises:**
  **ValueError** – If the “nutrition” column is missing from the recipes DataFrame.

#### generate_report(result: [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult), path)

Generate and save the nutrition feature outputs (stub implementation).

Saves the computed feature table to a CSV file in the given directory,
and returns the file paths and summary information.

* **Parameters:**
  * **result** ([*AnalysisResult*](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult)) – The result object returned by the analyze method, containing
    a DataFrame (result.table) and a summary dictionary.
  * **path** (*Path* *or* *str*) – Destination folder path where the output CSV will be written.
* **Returns:**
  Dictionary containing:
  - “table_path”: path to the saved CSV file.
  - “summary”: the summary statistics dictionary.
* **Return type:**
  dict[str, object]

## mangetamain.preprocessing.feature.nutrition.strategies module

Nutrition strategies (stubs).

Lightweight strategy placeholders for the nutrition feature pipeline. These
classes implement the minimal cleaning and preprocessing interfaces and can be
extended to handle missing values, standardize units, or normalize schemas.

### *class* mangetamain.preprocessing.feature.nutrition.strategies.NutritionCleaning(\*args, \*\*kwargs)

Bases: [`ICleaningStrategy`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.ICleaningStrategy)

No-op cleaning for nutrition inputs.

Potential responsibilities include dropping rows with malformed
`nutrition` fields or coercing numeric types.

#### clean(recipes: DataFrame, interactions: DataFrame) → tuple[DataFrame, DataFrame]

Return cleaned copies of the inputs.

* **Parameters:**
  * **recipes** – Recipes dataframe.
  * **interactions** – Interactions dataframe (unused here).
* **Returns:**
  Tuple of possibly transformed `(recipes, interactions)`.

### *class* mangetamain.preprocessing.feature.nutrition.strategies.NutritionPreprocessing(\*args, \*\*kwargs)

Bases: [`IPreprocessingStrategy`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.IPreprocessingStrategy)

No-op preprocessing for nutrition inputs.

Could expand list-like nutrition fields to structured columns or compute
derived fields required by downstream analysers.

#### preprocess(recipes: DataFrame, interactions: DataFrame) → tuple[DataFrame, DataFrame]

Return preprocessed copies of the inputs.

* **Parameters:**
  * **recipes** – Recipes dataframe.
  * **interactions** – Interactions dataframe (unused here).
* **Returns:**
  Tuple of possibly transformed `(recipes, interactions)`.

## Module contents

Nutrition module stubs.

### *class* mangetamain.preprocessing.feature.nutrition.NutritionCleaning(\*args, \*\*kwargs)

Bases: [`ICleaningStrategy`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.ICleaningStrategy)

No-op cleaning for nutrition inputs.

Potential responsibilities include dropping rows with malformed
`nutrition` fields or coercing numeric types.

#### clean(recipes: DataFrame, interactions: DataFrame) → tuple[DataFrame, DataFrame]

Return cleaned copies of the inputs.

* **Parameters:**
  * **recipes** – Recipes dataframe.
  * **interactions** – Interactions dataframe (unused here).
* **Returns:**
  Tuple of possibly transformed `(recipes, interactions)`.

### *class* mangetamain.preprocessing.feature.nutrition.NutritionPreprocessing(\*args, \*\*kwargs)

Bases: [`IPreprocessingStrategy`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.IPreprocessingStrategy)

No-op preprocessing for nutrition inputs.

Could expand list-like nutrition fields to structured columns or compute
derived fields required by downstream analysers.

#### preprocess(recipes: DataFrame, interactions: DataFrame) → tuple[DataFrame, DataFrame]

Return preprocessed copies of the inputs.

* **Parameters:**
  * **recipes** – Recipes dataframe.
  * **interactions** – Interactions dataframe (unused here).
* **Returns:**
  Tuple of possibly transformed `(recipes, interactions)`.

### *class* mangetamain.preprocessing.feature.nutrition.NutritionAnalyser

Bases: [`Analyser`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.Analyser)

Analyser computing nutrition-based features from recipe metadata.

This analyser extracts structured nutritional data (e.g., calories, fat,
protein, sugar) from the “nutrition” field of the recipes DataFrame.
It computes several derived indicators useful for downstream modeling
or recommendation tasks, such as energy density and nutrient balance.

### None explicitly defined — this class is stateless.

#### analyze(recipes: DataFrame, interactions: DataFrame | None = None, \*\*kwargs: object) → [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult)

Compute nutrition-based features for each recipe.

This method parses the “nutrition” field of the recipes DataFrame,
extracts individual nutrient values, and derives higher-level
indicators summarizing the nutritional composition of each recipe.

The computed features include:
- **energy_density**: ratio of calories to total macronutrients (fat + carbs + protein).
- **protein_ratio**: fraction of calories contributed by proteins.
- **fat_ratio**: fraction of calories contributed by fats.
- **nutrient_balance_index**: heuristic index combining protein and negative nutrients

> (fat, sugar, sodium) normalized by total calories.
* **Parameters:**
  * **recipes** (*pd.DataFrame*) – DataFrame containing recipe metadata.
    Must include a “nutrition” column, typically a stringified list such as:
    “[calories, fat, sugar, sodium, protein, sat_fat, carbs]”.
  * **interactions** (*pd.DataFrame* *,* *optional*) – DataFrame of user interactions (unused in this analyser, kept for interface compatibility).
  * **\*\*kwargs** (*object*) – Additional arguments passed for interface consistency (ignored).
* **Returns:**
  Object containing:
  - **table**: a DataFrame with one row per recipe and the computed nutrition features.
  - **summary**: a dictionary of global mean values and recipe count.
* **Return type:**
  [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult)
* **Raises:**
  **ValueError** – If the “nutrition” column is missing from the recipes DataFrame.

#### generate_report(result: [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult), path)

Generate and save the nutrition feature outputs (stub implementation).

Saves the computed feature table to a CSV file in the given directory,
and returns the file paths and summary information.

* **Parameters:**
  * **result** ([*AnalysisResult*](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult)) – The result object returned by the analyze method, containing
    a DataFrame (result.table) and a summary dictionary.
  * **path** (*Path* *or* *str*) – Destination folder path where the output CSV will be written.
* **Returns:**
  Dictionary containing:
  - “table_path”: path to the saved CSV file.
  - “summary”: the summary statistics dictionary.
* **Return type:**
  dict[str, object]
