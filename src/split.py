from __future__ import annotations

import numpy as np
import pandas as pd

TARGET = "sales"


def fixed_temporal_split(
    df: pd.DataFrame,
    features: list[str],
    train_end: pd.Timestamp,
    val_start: pd.Timestamp,
    val_end: pd.Timestamp,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    """
    Split a time series DataFrame into training and validation sets using fixed dates.

    Performs a chronological split with no overlap between train and validation,
    preventing data leakage. The split boundaries are defined explicitly by date
    rather than by row index or percentage, ensuring reproducibility across
    experiments regardless of dataset size.

    This function is used in NB4 for single-split evaluation. For a more robust
    estimate of model performance across time, use walk-forward cross-validation
    as implemented in NB5.

    Args:
        df:        DataFrame sorted by (store_nbr, family, date), with all
                   features and the target column already computed.
        features:  List of column names to use as model input features.
        train_end: Last date (inclusive) of the training window.
        val_start: First date (inclusive) of the validation window.
        val_end:   Last date (inclusive) of the validation window.

    Returns:
        A tuple of six elements:
            - train_data: full training DataFrame (all columns)
            - val_data:   full validation DataFrame (all columns)
            - X_train:    training feature matrix
            - y_train:    training target series
            - X_val:      validation feature matrix
            - y_val:      validation target series

    Example:
        >>> train_data, val_data, X_train, y_train, X_val, y_val = fixed_temporal_split(
        ...     df=advanced_train,
        ...     features=advanced_features,
        ...     train_end=pd.Timestamp("2017-06-04"),
        ...     val_start=pd.Timestamp("2017-06-05"),
        ...     val_end=pd.Timestamp("2017-08-15"),
        ... )
    """
    train_data = df[df["date"] <= train_end].copy()
    val_data = df[(df["date"] >= val_start) & (df["date"] <= val_end)].copy()

    X_train = train_data[features]
    y_train = train_data[TARGET]

    X_val = val_data[features]
    y_val = val_data[TARGET]

    return train_data, val_data, X_train, y_train, X_val, y_val

def build_walk_forward_folds(
    df: pd.DataFrame,
    n_folds: int = 4,
    val_size: int = 28,
    min_train_days: int = 365,
) -> list[dict]:
    """
    Build anchored walk-forward validation folds from a time series DataFrame.

    Each fold:
        - trains on all data available up to train_end
        - validates on the next val_size days
        - moves forward toward the most recent period

    This function is used for robust temporal validation on full-data experiments.

    Args:
        df: DataFrame containing a 'date' column.
        n_folds: Number of validation folds to build.
        val_size: Validation window size in days.
        min_train_days: Minimum number of historical dates required before validation.

    Returns:
        List of dictionaries with:
            - fold
            - train_end
            - val_start
            - val_end
    """
    unique_dates = np.array(sorted(df["date"].unique()))
    folds = []

    last_val_end_idx = len(unique_dates) - 1

    for i in range(n_folds):
        offset = (n_folds - 1 - i) * val_size

        val_end_idx = last_val_end_idx - offset
        val_start_idx = val_end_idx - val_size + 1
        train_end_idx = val_start_idx - 1

        if train_end_idx < min_train_days:
            break

        folds.append(
            {
                "fold": i + 1,
                "train_end": unique_dates[train_end_idx],
                "val_start": unique_dates[val_start_idx],
                "val_end": unique_dates[val_end_idx],
            }
        )

    return folds


def split_by_fold(
    df: pd.DataFrame,
    features: list[str],
    fold_info: dict,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    """
    Split data into train and validation sets using a single walk-forward fold.

    Args:
        df: DataFrame containing features, target and date column.
        features: List of feature columns.
        fold_info: Dictionary produced by build_walk_forward_folds().

    Returns:
        Same output structure as fixed_temporal_split().
    """
    return fixed_temporal_split(
        df=df,
        features=features,
        train_end=fold_info["train_end"],
        val_start=fold_info["val_start"],
        val_end=fold_info["val_end"],
    )