# mangetamain.clustering package

## Submodules

## mangetamain.clustering.pipeline module

Clustering pipeline (PCA + KMeans) for recipe feature tables.

This module loads precomputed feature tables produced by the preprocessing
analysers (nutrition, seasonality, rating, steps/complexity, ingredients),
validates the presence of required columns, and runs a dimensionality
reduction and clustering workflow that mirrors the team notebooks:

- merges inputs on recipe index,
- standardizes selected variables,
- computes PCA with as many components as features,
- applies KMeans to the first N principal components,
- exports a compact CSV with `cluster`, `pc_1` and `pc_2` per recipe.

See [`RecipeClusteringPipeline`](#mangetamain.clustering.pipeline.RecipeClusteringPipeline) for the public API.

### *class* mangetamain.clustering.pipeline.ClusteringPaths(base: Path = PosixPath('data/preprocessed'), out_dir: Path = PosixPath('data/clustering'), nutrition: str = 'nutrition_table.csv', seasonality: str = 'seasonality_table.csv', rating: str = 'rating_table.csv', complexity: str = 'complexity_table.csv', ingredients: str = 'ingredients_table.csv')

Bases: `object`

Input and output paths for clustering pipeline.

#### base *: Path* *= PosixPath('data/preprocessed')*

#### out_dir *: Path* *= PosixPath('data/clustering')*

#### nutrition *: str* *= 'nutrition_table.csv'*

#### seasonality *: str* *= 'seasonality_table.csv'*

#### rating *: str* *= 'rating_table.csv'*

#### complexity *: str* *= 'complexity_table.csv'*

#### ingredients *: str* *= 'ingredients_table.csv'*

#### input_paths() → dict[str, Path]

#### output_csv() → Path

#### \_\_init_\_(base: Path = PosixPath('data/preprocessed'), out_dir: Path = PosixPath('data/clustering'), nutrition: str = 'nutrition_table.csv', seasonality: str = 'seasonality_table.csv', rating: str = 'rating_table.csv', complexity: str = 'complexity_table.csv', ingredients: str = 'ingredients_table.csv') → None

### *class* mangetamain.clustering.pipeline.RecipeClusteringPipeline(\*, paths: [ClusteringPaths](#mangetamain.clustering.pipeline.ClusteringPaths) | None = None, logger: Logger | None = None, n_clusters: int = 5, random_state: int = 42, n_pcs_for_kmeans: int = 12)

Bases: `object`

Compute PCA and KMeans clustering from preprocessed feature CSVs.

This reproduces the notebook logic:
: - merge inputs on index
  - StandardScaler on REQUIRED_FEATURES
  - PCA with n_components = len(REQUIRED_FEATURES)
  - KMeans(n_clusters=5, random_state=42) on first 12 PCs
  - Output dataframe with per-recipe cluster, pc_1, pc_2

#### \_\_init_\_(\*, paths: [ClusteringPaths](#mangetamain.clustering.pipeline.ClusteringPaths) | None = None, logger: Logger | None = None, n_clusters: int = 5, random_state: int = 42, n_pcs_for_kmeans: int = 12) → None

#### run() → DataFrame

Execute the full clustering pipeline and save the CSV output.

* **Returns:**
  DataFrame indexed by recipe id with columns:
  : - name (if available)
    - cluster (int)
    - pc_1 (float)
    - pc_2 (float)
* **Return type:**
  pd.DataFrame

## Module contents

Clustering pipeline for recipe feature space (PCA + KMeans).

This submodule mirrors the structure and conventions used in
`mangetamain.preprocessing` while implementing the logic from the
`notebooks/EDA_recipes_clustering.ipynb` notebook.

### *class* mangetamain.clustering.RecipeClusteringPipeline(\*, paths: [ClusteringPaths](#mangetamain.clustering.pipeline.ClusteringPaths) | None = None, logger: Logger | None = None, n_clusters: int = 5, random_state: int = 42, n_pcs_for_kmeans: int = 12)

Bases: `object`

Compute PCA and KMeans clustering from preprocessed feature CSVs.

This reproduces the notebook logic:
: - merge inputs on index
  - StandardScaler on REQUIRED_FEATURES
  - PCA with n_components = len(REQUIRED_FEATURES)
  - KMeans(n_clusters=5, random_state=42) on first 12 PCs
  - Output dataframe with per-recipe cluster, pc_1, pc_2

#### \_\_init_\_(\*, paths: [ClusteringPaths](#mangetamain.clustering.pipeline.ClusteringPaths) | None = None, logger: Logger | None = None, n_clusters: int = 5, random_state: int = 42, n_pcs_for_kmeans: int = 12) → None

#### run() → DataFrame

Execute the full clustering pipeline and save the CSV output.

* **Returns:**
  DataFrame indexed by recipe id with columns:
  : - name (if available)
    - cluster (int)
    - pc_1 (float)
    - pc_2 (float)
* **Return type:**
  pd.DataFrame

### *class* mangetamain.clustering.ClusteringPaths(base: Path = PosixPath('data/preprocessed'), out_dir: Path = PosixPath('data/clustering'), nutrition: str = 'nutrition_table.csv', seasonality: str = 'seasonality_table.csv', rating: str = 'rating_table.csv', complexity: str = 'complexity_table.csv', ingredients: str = 'ingredients_table.csv')

Bases: `object`

Input and output paths for clustering pipeline.

#### base *: Path* *= PosixPath('data/preprocessed')*

#### out_dir *: Path* *= PosixPath('data/clustering')*

#### nutrition *: str* *= 'nutrition_table.csv'*

#### seasonality *: str* *= 'seasonality_table.csv'*

#### rating *: str* *= 'rating_table.csv'*

#### complexity *: str* *= 'complexity_table.csv'*

#### ingredients *: str* *= 'ingredients_table.csv'*

#### input_paths() → dict[str, Path]

#### output_csv() → Path

#### \_\_init_\_(base: Path = PosixPath('data/preprocessed'), out_dir: Path = PosixPath('data/clustering'), nutrition: str = 'nutrition_table.csv', seasonality: str = 'seasonality_table.csv', rating: str = 'rating_table.csv', complexity: str = 'complexity_table.csv', ingredients: str = 'ingredients_table.csv') → None
