import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class RecipeSeasonalityFeatureBuilder(BaseEstimator, TransformerMixin):
    """
    Transformer that computes seasonality features for recipes based on user
    interaction data.
    """

    def __init__(self, date_col="date", group_col="recipe_id", k=5.0):
        """
        Parameters
        ----------
        date_col : str
            Name of the date column in the interactions DataFrame.
        group_col : str
            Name of the column used to group interactions (e.g., recipe_id).
        k : float
            Empirical Bayes smoothing strength. Higher values apply stronger shrinkage
            toward the global seasonal mean.
        """
        self.date_col = date_col
        self.group_col = group_col
        self.k = k

        # Attributes learned during fit
        self.feature_df_ = None
        self.sin_global_ = None
        self.cos_global_ = None

    def fit(self, X: pd.DataFrame, y=None):
        """
        Learn seasonal interaction patterns from the interactions table.

        Parameters
        ----------
        X : pd.DataFrame
            Interaction table containing at least date_col and group_col.
        y : ignored
            Not used (exists for sklearn compatibility).

        Returns
        -------
        self : object
            Fitted transformer.
        """
        X = X.copy()

        # Validate required columns
        if self.date_col not in X.columns or self.group_col not in X.columns:
            raise ValueError(f"X must contain '{self.date_col}' and '{self.group_col}'")

        # Convert date column to datetime and compute day-of-year
        X[self.date_col] = pd.to_datetime(X[self.date_col], errors="coerce")
        if X[self.date_col].isna().any():
            raise ValueError(f"Invalid dates found in '{self.date_col}'")

        doy = X[self.date_col].dt.dayofyear
        X["doy_sin"] = np.sin(2 * np.pi * doy / 365)
        X["doy_cos"] = np.cos(2 * np.pi * doy / 365)

        # Compute global sine/cosine averages for smoothing
        self.sin_global_ = X["doy_sin"].mean()
        self.cos_global_ = X["doy_cos"].mean()

        # Aggregate per recipe_id
        agg = (
            X.groupby(self.group_col)
            .agg(
                sin_mean=("doy_sin", "mean"),
                cos_mean=("doy_cos", "mean"),
                n=("doy_sin", "size"),
            )
            .reset_index()
        )

        # Empirical Bayes smoothing
        agg["inter_doy_sin_smooth"] = (
            agg["n"] * agg["sin_mean"] + self.k * self.sin_global_
        ) / (agg["n"] + self.k)

        agg["inter_doy_cos_smooth"] = (
            agg["n"] * agg["cos_mean"] + self.k * self.cos_global_
        ) / (agg["n"] + self.k)

        # Compute seasonal strength (vector length)
        agg["inter_strength"] = np.sqrt(
            agg["inter_doy_sin_smooth"] ** 2 + agg["inter_doy_cos_smooth"] ** 2
        )

        # Store only the aggregated features for merging later
        self.feature_df_ = agg[
            [
                self.group_col,
                "inter_doy_sin_smooth",
                "inter_doy_cos_smooth",
                "inter_strength",
            ]
        ]

        return self

    def transform(self, X: pd.DataFrame):
        """
        Merge the precomputed seasonality features into the recipes DataFrame.

        Parameters
        ----------
        X : pd.DataFrame
            Recipes table containing group_col (e.g., recipe_id).

        Returns
        -------
        X_out : pd.DataFrame
            Recipes table with added seasonality feature columns.
        """
        if self.feature_df_ is None:
            raise RuntimeError("Must fit on interactions before transforming recipes")

        X_out = X.copy()

        # Merge seasonal features into recipes
        X_out = X_out.merge(
            self.feature_df_, left_on="id", right_on=self.group_col, how="left"
        )

        # Fill missing recipes (not seen in interactions) with global values
        X_out["inter_doy_sin_smooth"] = X_out["inter_doy_sin_smooth"].fillna(
            self.sin_global_
        )
        X_out["inter_doy_cos_smooth"] = X_out["inter_doy_cos_smooth"].fillna(
            self.cos_global_
        )
        X_out["inter_strength"] = X_out["inter_strength"].fillna(0.0)

        return X_out
