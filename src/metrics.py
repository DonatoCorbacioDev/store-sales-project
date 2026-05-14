from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_squared_log_error,
    r2_score,
)


def evaluate_regression(y_true, y_pred) -> dict:
    """
    Compute a standard set of regression metrics for model evaluation.

    Calculates RMSLE, MAE, RMSE and R² in a single call, returning them
    as a flat dictionary ready to be logged directly to MLflow.

    Note: y_pred should be clipped to zero before calling this function,
    as RMSLE is undefined for negative values.

    Args:
        y_true: Array-like of true target values (non-negative).
        y_pred: Array-like of predicted values (non-negative).

    Returns:
        Dictionary with keys: 'rmsle', 'mae', 'rmse', 'r2'.
    """
    return {
        "rmsle": float(np.sqrt(mean_squared_log_error(y_true, y_pred))),
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "r2": float(r2_score(y_true, y_pred)),
    }


def build_validation_results(
    val_data: pd.DataFrame,
    y_pred: np.ndarray,
) -> pd.DataFrame:
    """
    Build a structured validation results DataFrame for error analysis.

    Combines ground truth and predictions into a single DataFrame,
    adding derived columns for error inspection and segment analysis.
    This output is used by compute_segment_metrics() and can be logged
    to MLflow as a CSV artifact.

    Columns added:
        - y_pred:      model predictions
        - error:       signed error (sales - y_pred)
        - abs_error:   absolute error
        - is_weekend:  1 if dayofweek in {5, 6}, else 0

    Args:
        val_data: Validation DataFrame containing at minimum the columns
                  date, store_nbr, family, dayofweek, month, sales, onpromotion.
        y_pred:   Array of predictions aligned with val_data index.

    Returns:
        DataFrame with original columns plus error-derived columns.
    """
    results = val_data[
        ["date", "store_nbr", "family", "dayofweek", "month", "sales", "onpromotion"]
    ].copy()

    results["y_pred"] = y_pred
    results["error"] = results["sales"] - results["y_pred"]
    results["abs_error"] = results["error"].abs()
    results["is_weekend"] = results["dayofweek"].isin([5, 6]).astype(int)

    return results


def compute_segment_metrics(results: pd.DataFrame) -> dict:
    """
    Compute MAE broken down by weekday and weekend segments.

    Segment-level metrics expose systematic model weaknesses that global
    metrics can hide. For example, a model may perform well on weekdays
    but poorly on weekends due to different sales dynamics.

    Requires build_validation_results() to have been called first,
    as it depends on the 'is_weekend' and 'abs_error' columns.

    Args:
        results: DataFrame produced by build_validation_results(),
                 with columns 'is_weekend' and 'abs_error'.

    Returns:
        Dictionary with keys: 'mae_weekday', 'mae_weekend'.
    """
    weekday_mae = results.loc[results["is_weekend"] == 0, "abs_error"].mean()
    weekend_mae = results.loc[results["is_weekend"] == 1, "abs_error"].mean()

    return {
        "mae_weekday": float(weekday_mae),
        "mae_weekend": float(weekend_mae),
    }