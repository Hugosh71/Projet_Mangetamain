# mangetamain.preprocessing.feature.rating package

## Submodules

## mangetamain.preprocessing.feature.rating.analyzers module

Analyzers for rating feature.

### *class* mangetamain.preprocessing.feature.rating.analyzers.RatingAnalyser(\*, logger: Logger | None = None)

Bases: [`Analyser`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.Analyser)

Produce high-level insights for ratings (top-K by mean, etc.).

#### \_\_init_\_(\*, logger: Logger | None = None) → None

#### analyze(recipes: DataFrame, interactions: DataFrame, \*, c: int | None = None, mu_percentile: float = 0.5, include_zero_ratings: bool = True, with_wilson_per_recipe: bool = False) → [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult)

Produce analysis artefacts from processed dataframes.

#### generate_report(result: [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult), path: Path) → dict[str, object]

Return a minimal, serializable representation of the result.

## mangetamain.preprocessing.feature.rating.strategies module

Strategies specific to rating feature processing.

### *class* mangetamain.preprocessing.feature.rating.strategies.RatingCleaning(\*args, \*\*kwargs)

Bases: [`ICleaningStrategy`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.ICleaningStrategy)

Remove zero and NA ratings to keep only informative interactions.

#### clean(recipes: DataFrame, interactions: DataFrame) → tuple[DataFrame, DataFrame]

### *class* mangetamain.preprocessing.feature.rating.strategies.RatingPreprocessing(\*args, \*\*kwargs)

Bases: [`IPreprocessingStrategy`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.IPreprocessingStrategy)

Add normalized rating column for downstream analysis.

#### preprocess(recipes: DataFrame, interactions: DataFrame) → tuple[DataFrame, DataFrame]
