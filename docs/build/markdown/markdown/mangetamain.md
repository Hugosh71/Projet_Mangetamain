# mangetamain package

## Subpackages

* [mangetamain.clustering package](mangetamain.clustering.md)
  * [Submodules](mangetamain.clustering.md#submodules)
  * [mangetamain.clustering.pipeline module](mangetamain.clustering.md#module-mangetamain.clustering.pipeline)
    * [`ClusteringPaths`](mangetamain.clustering.md#mangetamain.clustering.pipeline.ClusteringPaths)
      * [`ClusteringPaths.base`](mangetamain.clustering.md#mangetamain.clustering.pipeline.ClusteringPaths.base)
      * [`ClusteringPaths.out_dir`](mangetamain.clustering.md#mangetamain.clustering.pipeline.ClusteringPaths.out_dir)
      * [`ClusteringPaths.nutrition`](mangetamain.clustering.md#mangetamain.clustering.pipeline.ClusteringPaths.nutrition)
      * [`ClusteringPaths.seasonality`](mangetamain.clustering.md#mangetamain.clustering.pipeline.ClusteringPaths.seasonality)
      * [`ClusteringPaths.rating`](mangetamain.clustering.md#mangetamain.clustering.pipeline.ClusteringPaths.rating)
      * [`ClusteringPaths.complexity`](mangetamain.clustering.md#mangetamain.clustering.pipeline.ClusteringPaths.complexity)
      * [`ClusteringPaths.ingredients`](mangetamain.clustering.md#mangetamain.clustering.pipeline.ClusteringPaths.ingredients)
      * [`ClusteringPaths.input_paths()`](mangetamain.clustering.md#mangetamain.clustering.pipeline.ClusteringPaths.input_paths)
      * [`ClusteringPaths.output_csv()`](mangetamain.clustering.md#mangetamain.clustering.pipeline.ClusteringPaths.output_csv)
      * [`ClusteringPaths.__init__()`](mangetamain.clustering.md#mangetamain.clustering.pipeline.ClusteringPaths.__init__)
    * [`RecipeClusteringPipeline`](mangetamain.clustering.md#mangetamain.clustering.pipeline.RecipeClusteringPipeline)
      * [`RecipeClusteringPipeline.__init__()`](mangetamain.clustering.md#mangetamain.clustering.pipeline.RecipeClusteringPipeline.__init__)
      * [`RecipeClusteringPipeline.run()`](mangetamain.clustering.md#mangetamain.clustering.pipeline.RecipeClusteringPipeline.run)
  * [Module contents](mangetamain.clustering.md#module-mangetamain.clustering)
    * [`RecipeClusteringPipeline`](mangetamain.clustering.md#mangetamain.clustering.RecipeClusteringPipeline)
      * [`RecipeClusteringPipeline.__init__()`](mangetamain.clustering.md#mangetamain.clustering.RecipeClusteringPipeline.__init__)
      * [`RecipeClusteringPipeline.run()`](mangetamain.clustering.md#mangetamain.clustering.RecipeClusteringPipeline.run)
    * [`ClusteringPaths`](mangetamain.clustering.md#mangetamain.clustering.ClusteringPaths)
      * [`ClusteringPaths.base`](mangetamain.clustering.md#mangetamain.clustering.ClusteringPaths.base)
      * [`ClusteringPaths.out_dir`](mangetamain.clustering.md#mangetamain.clustering.ClusteringPaths.out_dir)
      * [`ClusteringPaths.nutrition`](mangetamain.clustering.md#mangetamain.clustering.ClusteringPaths.nutrition)
      * [`ClusteringPaths.seasonality`](mangetamain.clustering.md#mangetamain.clustering.ClusteringPaths.seasonality)
      * [`ClusteringPaths.rating`](mangetamain.clustering.md#mangetamain.clustering.ClusteringPaths.rating)
      * [`ClusteringPaths.complexity`](mangetamain.clustering.md#mangetamain.clustering.ClusteringPaths.complexity)
      * [`ClusteringPaths.ingredients`](mangetamain.clustering.md#mangetamain.clustering.ClusteringPaths.ingredients)
      * [`ClusteringPaths.input_paths()`](mangetamain.clustering.md#mangetamain.clustering.ClusteringPaths.input_paths)
      * [`ClusteringPaths.output_csv()`](mangetamain.clustering.md#mangetamain.clustering.ClusteringPaths.output_csv)
      * [`ClusteringPaths.__init__()`](mangetamain.clustering.md#mangetamain.clustering.ClusteringPaths.__init__)
* [mangetamain.preprocessing package](mangetamain.preprocessing.md)
  * [Subpackages](mangetamain.preprocessing.md#subpackages)
    * [mangetamain.preprocessing.feature package](mangetamain.preprocessing.feature.md)
      * [Subpackages](mangetamain.preprocessing.feature.md#subpackages)
      * [Module contents](mangetamain.preprocessing.feature.md#module-mangetamain.preprocessing.feature)
  * [Submodules](mangetamain.preprocessing.md#submodules)
  * [mangetamain.preprocessing.exceptions module](mangetamain.preprocessing.md#module-mangetamain.preprocessing.exceptions)
    * [`DataError`](mangetamain.preprocessing.md#mangetamain.preprocessing.exceptions.DataError)
    * [`DataNotFoundError`](mangetamain.preprocessing.md#mangetamain.preprocessing.exceptions.DataNotFoundError)
    * [`DataLoadError`](mangetamain.preprocessing.md#mangetamain.preprocessing.exceptions.DataLoadError)
    * [`ValidationError`](mangetamain.preprocessing.md#mangetamain.preprocessing.exceptions.ValidationError)
  * [mangetamain.preprocessing.factories module](mangetamain.preprocessing.md#module-mangetamain.preprocessing.factories)
    * [`ProcessorFactory`](mangetamain.preprocessing.md#mangetamain.preprocessing.factories.ProcessorFactory)
      * [`ProcessorFactory.create_basic()`](mangetamain.preprocessing.md#mangetamain.preprocessing.factories.ProcessorFactory.create_basic)
      * [`ProcessorFactory.create_rating()`](mangetamain.preprocessing.md#mangetamain.preprocessing.factories.ProcessorFactory.create_rating)
      * [`ProcessorFactory.create_seasonality()`](mangetamain.preprocessing.md#mangetamain.preprocessing.factories.ProcessorFactory.create_seasonality)
      * [`ProcessorFactory.create_ingredients()`](mangetamain.preprocessing.md#mangetamain.preprocessing.factories.ProcessorFactory.create_ingredients)
      * [`ProcessorFactory.create_nutrition()`](mangetamain.preprocessing.md#mangetamain.preprocessing.factories.ProcessorFactory.create_nutrition)
      * [`ProcessorFactory.create_steps()`](mangetamain.preprocessing.md#mangetamain.preprocessing.factories.ProcessorFactory.create_steps)
  * [mangetamain.preprocessing.feature_engineering module](mangetamain.preprocessing.md#module-mangetamain.preprocessing.feature_engineering)
    * [`RecipeSeasonalityFeatureBuilder`](mangetamain.preprocessing.md#mangetamain.preprocessing.feature_engineering.RecipeSeasonalityFeatureBuilder)
      * [`RecipeSeasonalityFeatureBuilder.__init__()`](mangetamain.preprocessing.md#mangetamain.preprocessing.feature_engineering.RecipeSeasonalityFeatureBuilder.__init__)
      * [`RecipeSeasonalityFeatureBuilder.fit()`](mangetamain.preprocessing.md#mangetamain.preprocessing.feature_engineering.RecipeSeasonalityFeatureBuilder.fit)
      * [`RecipeSeasonalityFeatureBuilder.transform()`](mangetamain.preprocessing.md#mangetamain.preprocessing.feature_engineering.RecipeSeasonalityFeatureBuilder.transform)
  * [mangetamain.preprocessing.interfaces module](mangetamain.preprocessing.md#module-mangetamain.preprocessing.interfaces)
    * [`IDataRepository`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.IDataRepository)
      * [`IDataRepository.load_recipes()`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.IDataRepository.load_recipes)
      * [`IDataRepository.load_interactions()`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.IDataRepository.load_interactions)
    * [`IValidator`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.IValidator)
      * [`IValidator.validate()`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.IValidator.validate)
    * [`ICleaningStrategy`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.ICleaningStrategy)
      * [`ICleaningStrategy.clean()`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.ICleaningStrategy.clean)
      * [`ICleaningStrategy.__init__()`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.ICleaningStrategy.__init__)
    * [`IPreprocessingStrategy`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.IPreprocessingStrategy)
      * [`IPreprocessingStrategy.preprocess()`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.IPreprocessingStrategy.preprocess)
      * [`IPreprocessingStrategy.__init__()`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.IPreprocessingStrategy.__init__)
    * [`ProcessedPair`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.ProcessedPair)
      * [`ProcessedPair.recipes`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.ProcessedPair.recipes)
      * [`ProcessedPair.interactions`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.ProcessedPair.interactions)
      * [`ProcessedPair.__init__()`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.ProcessedPair.__init__)
    * [`AnalysisResult`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult)
      * [`AnalysisResult.table`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult.table)
      * [`AnalysisResult.summary`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult.summary)
      * [`AnalysisResult.__init__()`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.AnalysisResult.__init__)
    * [`Analyser`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.Analyser)
      * [`Analyser.analyze()`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.Analyser.analyze)
      * [`Analyser.generate_report()`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.Analyser.generate_report)
    * [`DataProcessor`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.DataProcessor)
      * [`DataProcessor.__init__()`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.DataProcessor.__init__)
      * [`DataProcessor.clean()`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.DataProcessor.clean)
      * [`DataProcessor.preprocess()`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.DataProcessor.preprocess)
      * [`DataProcessor.run()`](mangetamain.preprocessing.md#mangetamain.preprocessing.interfaces.DataProcessor.run)
  * [mangetamain.preprocessing.processors module](mangetamain.preprocessing.md#module-mangetamain.preprocessing.processors)
    * [`NoOpCleaning`](mangetamain.preprocessing.md#mangetamain.preprocessing.processors.NoOpCleaning)
      * [`NoOpCleaning.clean()`](mangetamain.preprocessing.md#mangetamain.preprocessing.processors.NoOpCleaning.clean)
    * [`NoOpPreprocessing`](mangetamain.preprocessing.md#mangetamain.preprocessing.processors.NoOpPreprocessing)
      * [`NoOpPreprocessing.preprocess()`](mangetamain.preprocessing.md#mangetamain.preprocessing.processors.NoOpPreprocessing.preprocess)
    * [`BasicDataProcessor`](mangetamain.preprocessing.md#mangetamain.preprocessing.processors.BasicDataProcessor)
      * [`BasicDataProcessor.__init__()`](mangetamain.preprocessing.md#mangetamain.preprocessing.processors.BasicDataProcessor.__init__)
      * [`BasicDataProcessor.clean()`](mangetamain.preprocessing.md#mangetamain.preprocessing.processors.BasicDataProcessor.clean)
      * [`BasicDataProcessor.preprocess()`](mangetamain.preprocessing.md#mangetamain.preprocessing.processors.BasicDataProcessor.preprocess)
  * [mangetamain.preprocessing.repositories module](mangetamain.preprocessing.md#module-mangetamain.preprocessing.repositories)
    * [`RepositoryPaths`](mangetamain.preprocessing.md#mangetamain.preprocessing.repositories.RepositoryPaths)
      * [`RepositoryPaths.recipes_csv`](mangetamain.preprocessing.md#mangetamain.preprocessing.repositories.RepositoryPaths.recipes_csv)
      * [`RepositoryPaths.interactions_csv`](mangetamain.preprocessing.md#mangetamain.preprocessing.repositories.RepositoryPaths.interactions_csv)
      * [`RepositoryPaths.__init__()`](mangetamain.preprocessing.md#mangetamain.preprocessing.repositories.RepositoryPaths.__init__)
    * [`CSVDataRepository`](mangetamain.preprocessing.md#mangetamain.preprocessing.repositories.CSVDataRepository)
      * [`CSVDataRepository.__init__()`](mangetamain.preprocessing.md#mangetamain.preprocessing.repositories.CSVDataRepository.__init__)
      * [`CSVDataRepository.load_recipes()`](mangetamain.preprocessing.md#mangetamain.preprocessing.repositories.CSVDataRepository.load_recipes)
      * [`CSVDataRepository.load_interactions()`](mangetamain.preprocessing.md#mangetamain.preprocessing.repositories.CSVDataRepository.load_interactions)
  * [mangetamain.preprocessing.streamlit module](mangetamain.preprocessing.md#module-mangetamain.preprocessing.streamlit)
    * [`load_recipes_data()`](mangetamain.preprocessing.md#mangetamain.preprocessing.streamlit.load_recipes_data)
    * [`get_cluster_names()`](mangetamain.preprocessing.md#mangetamain.preprocessing.streamlit.get_cluster_names)
    * [`get_col_names()`](mangetamain.preprocessing.md#mangetamain.preprocessing.streamlit.get_col_names)
    * [`remove_outliers_iqr()`](mangetamain.preprocessing.md#mangetamain.preprocessing.streamlit.remove_outliers_iqr)
    * [`add_month_labels()`](mangetamain.preprocessing.md#mangetamain.preprocessing.streamlit.add_month_labels)
    * [`rgb_to_hex()`](mangetamain.preprocessing.md#mangetamain.preprocessing.streamlit.rgb_to_hex)
    * [`min_max_scale()`](mangetamain.preprocessing.md#mangetamain.preprocessing.streamlit.min_max_scale)
    * [`get_tag_cloud()`](mangetamain.preprocessing.md#mangetamain.preprocessing.streamlit.get_tag_cloud)
    * [`get_cluster_summary()`](mangetamain.preprocessing.md#mangetamain.preprocessing.streamlit.get_cluster_summary)
  * [Module contents](mangetamain.preprocessing.md#module-mangetamain.preprocessing)
    * [`IDataRepository`](mangetamain.preprocessing.md#mangetamain.preprocessing.IDataRepository)
      * [`IDataRepository.load_recipes()`](mangetamain.preprocessing.md#mangetamain.preprocessing.IDataRepository.load_recipes)
      * [`IDataRepository.load_interactions()`](mangetamain.preprocessing.md#mangetamain.preprocessing.IDataRepository.load_interactions)
    * [`IValidator`](mangetamain.preprocessing.md#mangetamain.preprocessing.IValidator)
      * [`IValidator.validate()`](mangetamain.preprocessing.md#mangetamain.preprocessing.IValidator.validate)
    * [`DataProcessor`](mangetamain.preprocessing.md#mangetamain.preprocessing.DataProcessor)
      * [`DataProcessor.__init__()`](mangetamain.preprocessing.md#mangetamain.preprocessing.DataProcessor.__init__)
      * [`DataProcessor.clean()`](mangetamain.preprocessing.md#mangetamain.preprocessing.DataProcessor.clean)
      * [`DataProcessor.preprocess()`](mangetamain.preprocessing.md#mangetamain.preprocessing.DataProcessor.preprocess)
      * [`DataProcessor.run()`](mangetamain.preprocessing.md#mangetamain.preprocessing.DataProcessor.run)
    * [`Analyser`](mangetamain.preprocessing.md#mangetamain.preprocessing.Analyser)
      * [`Analyser.analyze()`](mangetamain.preprocessing.md#mangetamain.preprocessing.Analyser.analyze)
      * [`Analyser.generate_report()`](mangetamain.preprocessing.md#mangetamain.preprocessing.Analyser.generate_report)
    * [`AnalysisResult`](mangetamain.preprocessing.md#mangetamain.preprocessing.AnalysisResult)
      * [`AnalysisResult.table`](mangetamain.preprocessing.md#mangetamain.preprocessing.AnalysisResult.table)
      * [`AnalysisResult.summary`](mangetamain.preprocessing.md#mangetamain.preprocessing.AnalysisResult.summary)
      * [`AnalysisResult.__init__()`](mangetamain.preprocessing.md#mangetamain.preprocessing.AnalysisResult.__init__)
    * [`ICleaningStrategy`](mangetamain.preprocessing.md#mangetamain.preprocessing.ICleaningStrategy)
      * [`ICleaningStrategy.clean()`](mangetamain.preprocessing.md#mangetamain.preprocessing.ICleaningStrategy.clean)
      * [`ICleaningStrategy.__init__()`](mangetamain.preprocessing.md#mangetamain.preprocessing.ICleaningStrategy.__init__)
    * [`IPreprocessingStrategy`](mangetamain.preprocessing.md#mangetamain.preprocessing.IPreprocessingStrategy)
      * [`IPreprocessingStrategy.preprocess()`](mangetamain.preprocessing.md#mangetamain.preprocessing.IPreprocessingStrategy.preprocess)
      * [`IPreprocessingStrategy.__init__()`](mangetamain.preprocessing.md#mangetamain.preprocessing.IPreprocessingStrategy.__init__)
    * [`DataError`](mangetamain.preprocessing.md#mangetamain.preprocessing.DataError)
    * [`DataNotFoundError`](mangetamain.preprocessing.md#mangetamain.preprocessing.DataNotFoundError)
    * [`DataLoadError`](mangetamain.preprocessing.md#mangetamain.preprocessing.DataLoadError)
    * [`ValidationError`](mangetamain.preprocessing.md#mangetamain.preprocessing.ValidationError)
    * [`RepositoryPaths`](mangetamain.preprocessing.md#mangetamain.preprocessing.RepositoryPaths)
      * [`RepositoryPaths.recipes_csv`](mangetamain.preprocessing.md#mangetamain.preprocessing.RepositoryPaths.recipes_csv)
      * [`RepositoryPaths.interactions_csv`](mangetamain.preprocessing.md#mangetamain.preprocessing.RepositoryPaths.interactions_csv)
      * [`RepositoryPaths.__init__()`](mangetamain.preprocessing.md#mangetamain.preprocessing.RepositoryPaths.__init__)
    * [`CSVDataRepository`](mangetamain.preprocessing.md#mangetamain.preprocessing.CSVDataRepository)
      * [`CSVDataRepository.__init__()`](mangetamain.preprocessing.md#mangetamain.preprocessing.CSVDataRepository.__init__)
      * [`CSVDataRepository.load_recipes()`](mangetamain.preprocessing.md#mangetamain.preprocessing.CSVDataRepository.load_recipes)
      * [`CSVDataRepository.load_interactions()`](mangetamain.preprocessing.md#mangetamain.preprocessing.CSVDataRepository.load_interactions)
    * [`BasicDataProcessor`](mangetamain.preprocessing.md#mangetamain.preprocessing.BasicDataProcessor)
      * [`BasicDataProcessor.__init__()`](mangetamain.preprocessing.md#mangetamain.preprocessing.BasicDataProcessor.__init__)
      * [`BasicDataProcessor.clean()`](mangetamain.preprocessing.md#mangetamain.preprocessing.BasicDataProcessor.clean)
      * [`BasicDataProcessor.preprocess()`](mangetamain.preprocessing.md#mangetamain.preprocessing.BasicDataProcessor.preprocess)
    * [`ProcessorFactory`](mangetamain.preprocessing.md#mangetamain.preprocessing.ProcessorFactory)
      * [`ProcessorFactory.create_basic()`](mangetamain.preprocessing.md#mangetamain.preprocessing.ProcessorFactory.create_basic)
      * [`ProcessorFactory.create_rating()`](mangetamain.preprocessing.md#mangetamain.preprocessing.ProcessorFactory.create_rating)
      * [`ProcessorFactory.create_seasonality()`](mangetamain.preprocessing.md#mangetamain.preprocessing.ProcessorFactory.create_seasonality)
      * [`ProcessorFactory.create_ingredients()`](mangetamain.preprocessing.md#mangetamain.preprocessing.ProcessorFactory.create_ingredients)
      * [`ProcessorFactory.create_nutrition()`](mangetamain.preprocessing.md#mangetamain.preprocessing.ProcessorFactory.create_nutrition)
      * [`ProcessorFactory.create_steps()`](mangetamain.preprocessing.md#mangetamain.preprocessing.ProcessorFactory.create_steps)

## Submodules

## mangetamain.core module

Core utilities for Mangetamain.

This module provides essential configuration and utility functions for the
Mangetamain application. It includes the main configuration class and
helper functions for application setup.

### *class* mangetamain.core.AppConfig(name: str = 'Mangetamain', version: str = '0.1.0')

Bases: `object`

Application configuration container.

This class holds the core configuration settings for the Mangetamain
application. It uses a frozen dataclass to ensure immutability and
type safety.

#### name

The name of the application. Defaults to “Mangetamain”.

* **Type:**
  str

#### version

The version of the application. Defaults to “0.1.0”.

* **Type:**
  str

### Example

```pycon
>>> config = AppConfig()
>>> print(config.name)
Mangetamain
>>> print(config.version)
0.1.0
```

```pycon
>>> custom_config = AppConfig(name="MyApp", version="1.0.0")
>>> print(custom_config.name)
MyApp
```

#### name *: str* *= 'Mangetamain'*

#### version *: str* *= '0.1.0'*

#### \_\_init_\_(name: str = 'Mangetamain', version: str = '0.1.0') → None

### mangetamain.core.get_app_config() → [AppConfig](#mangetamain.core.AppConfig)

Return the default application configuration.

This function creates and returns a new AppConfig instance with
default values. It serves as the primary way to access application
configuration throughout the codebase.

* **Returns:**
  A new AppConfig instance with default values.
* **Return type:**
  [AppConfig](#mangetamain.core.AppConfig)

### Example

```pycon
>>> config = get_app_config()
>>> isinstance(config, AppConfig)
True
>>> config.name
'Mangetamain'
>>> config.version
'0.1.0'
```

## Module contents

Core package for the Mangetamain application.
