# mangetamain.preprocessing.feature.steps package

## Submodules

## mangetamain.preprocessing.feature.steps.analysers module

Steps analysers (stubs).

### *class* mangetamain.preprocessing.feature.steps.analysers.StepsAnalyser(\*, logger: Logger | None = None)

Bases: [`Analyser`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.Analyser)

#### \_\_init_\_(\*, logger: Logger | None = None) → None

#### analyze(recipes: DataFrame, interactions: DataFrame, \*\*kwargs: object) → [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult)

Produce analysis artefacts from processed dataframes.

#### generate_report(result: [AnalysisResult](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult), path: Path | str) → dict[str, object]

Génère les fichiers de rapport pour l’analyse des étapes.

## mangetamain.preprocessing.feature.steps.strategies module

Steps strategies (stubs).

### *class* mangetamain.preprocessing.feature.steps.strategies.StepsCleaning(\*args, \*\*kwargs)

Bases: [`ICleaningStrategy`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.ICleaningStrategy)

#### clean(recipes: DataFrame, interactions: DataFrame) → tuple[DataFrame, DataFrame]

### *class* mangetamain.preprocessing.feature.steps.strategies.StepsPreprocessing(\*args, \*\*kwargs)

Bases: [`IPreprocessingStrategy`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.IPreprocessingStrategy)

#### preprocess(recipes: DataFrame, interactions: DataFrame) → tuple[DataFrame, DataFrame]
