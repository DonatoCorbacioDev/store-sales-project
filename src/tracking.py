from __future__ import annotations

import json
import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
import mlflow
import pandas as pd


def log_feature_list(features: list[str], artifact_name: str = "features.json") -> None:
    """
    Log the list of model features as a JSON artifact to MLflow.

    Serializes the feature list to a temporary file and uploads it as an
    artifact to the active MLflow run. Useful for tracking exactly which
    features were used in each experiment, enabling reproducibility and
    side-by-side comparison across runs.

    Args:
        features:      Ordered list of feature column names used by the model.
        artifact_name: Name of the artifact file in MLflow. Defaults to
                       'features.json'.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / artifact_name
        with open(path, "w", encoding="utf-8") as f:
            json.dump(features, f, indent=2)
        mlflow.log_artifact(str(path))


def log_feature_importance(
    model,
    features: list[str],
    artifact_name: str,
) -> pd.Series:
    """
    Plot and log a feature importance bar chart as an MLflow artifact.

    Extracts feature importances from a fitted LightGBM model, plots the
    top 15 features, saves the chart to a temporary file, and uploads it
    to the active MLflow run. Also returns the full importance Series for
    further inspection or comparison between experiments.

    Args:
        model:         Fitted LGBMRegressor with a feature_importances_ attribute.
        features:      List of feature names aligned with model.feature_importances_.
        artifact_name: Name of the PNG file logged to MLflow (e.g.
                       'feature_importance.png').

    Returns:
        pandas Series of feature importances sorted in descending order,
        indexed by feature name.
    """
    importances = pd.Series(
        model.feature_importances_, index=features
    ).sort_values(ascending=False)

    plt.figure(figsize=(10, 5))
    importances.head(15).plot(kind="bar")
    plt.title("Top Feature Importances")
    plt.tight_layout()

    with tempfile.TemporaryDirectory() as tmpdir:
        plot_path = Path(tmpdir) / artifact_name
        plt.savefig(plot_path, bbox_inches="tight")
        plt.close()
        mlflow.log_artifact(str(plot_path))

    return importances


def log_run_context(
    train_data: pd.DataFrame,
    val_data: pd.DataFrame,
    features: list[str],
    feature_set_name: str,
    artifact_name: str = "run_context.json",
) -> None:
    """
    Log a structured summary of the experiment context as a JSON artifact.

    Captures the key metadata of a training run — date boundaries, split
    sizes, and feature set — in a single JSON file. This makes it possible
    to reconstruct the exact data configuration of any MLflow run without
    reading the notebook, which is essential for debugging regressions or
    comparing experiments months later.

    Args:
        train_data:       Full training DataFrame, used to extract date range
                          and row count.
        val_data:         Full validation DataFrame, used to extract date range
                          and row count.
        features:         List of feature column names used in the run.
        feature_set_name: Human-readable label for the feature set
                          (e.g. 'baseline_v1', 'advanced_v1').
        artifact_name:    Name of the JSON file logged to MLflow. Defaults to
                          'run_context.json'.
    """
    context = {
        "feature_set": feature_set_name,
        "train_start": str(train_data["date"].min()),
        "train_end": str(train_data["date"].max()),
        "val_start": str(val_data["date"].min()),
        "val_end": str(val_data["date"].max()),
        "n_train_rows": int(len(train_data)),
        "n_val_rows": int(len(val_data)),
        "n_features": int(len(features)),
        "features": features,
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / artifact_name
        with open(path, "w", encoding="utf-8") as f:
            json.dump(context, f, indent=2)
        mlflow.log_artifact(str(path))


def log_validation_predictions(
    results: pd.DataFrame,
    artifact_name: str = "validation_predictions.csv",
) -> None:
    """
    Log the validation predictions DataFrame as a CSV artifact to MLflow.

    Saves the full validation results table — including ground truth, predictions,
    and error columns — to a temporary CSV file and uploads it to the active
    MLflow run. This artifact enables post-hoc error analysis directly from
    the MLflow UI without re-running the notebook.

    Expects a DataFrame produced by build_validation_results() in metrics.py,
    which includes columns: date, store_nbr, family, sales, y_pred, error,
    abs_error, is_weekend.

    Args:
        results:       DataFrame of validation results to log.
        artifact_name: Name of the CSV file in MLflow. Defaults to
                       'validation_predictions.csv'.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / artifact_name
        results.to_csv(path, index=False)
        mlflow.log_artifact(str(path))