from __future__ import annotations

import numpy as np
import pandas as pd
from lightgbm import LGBMRegressor

from src.metrics import evaluate_regression

def evaluate_feature_set(
    df: pd.DataFrame,
    features: list[str],
    model_name: str,
    folds: list[dict],
    seed: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Train and evaluate LightGBM on walk-forward folds.

    This helper is used to compare multiple feature sets under the same
    validation strategy, ensuring a fair comparison between model variants.

    Args:
        df: Full dataset with target and features.
        features: Feature columns used for training.
        model_name: Label assigned to the evaluated feature set.
        folds: Walk-forward folds generated from split.py.
        seed: Random seed for reproducibility.

    Returns:
        Tuple:
            - metrics_df: metrics per fold
            - errors_df: validation predictions with error columns
    """
    all_metrics = []
    all_errors = []

    for fold_info in folds:
        fold = fold_info["fold"]
        train_end = fold_info["train_end"]
        val_start = fold_info["val_start"]
        val_end = fold_info["val_end"]

        train_fold = df[df["date"] <= train_end].copy()
        val_fold = df[
            (df["date"] >= val_start) &
            (df["date"] <= val_end)
        ].copy()

        X_train = train_fold[features]
        y_train = train_fold["sales"]

        X_val = val_fold[features]
        y_val = val_fold["sales"]

        model = LGBMRegressor(
            n_estimators=300,
            learning_rate=0.05,
            num_leaves=31,
            random_state=seed,
            n_jobs=-1,
        )

        model.fit(X_train, y_train)

        y_pred = model.predict(X_val)
        y_pred = np.clip(y_pred, 0, None)

        metrics = evaluate_regression(y_val, y_pred)
        metrics["fold"] = fold
        metrics["model"] = model_name
        all_metrics.append(metrics)

        fold_errors = val_fold.copy()
        fold_errors["model"] = model_name
        fold_errors["fold"] = fold
        fold_errors["y_pred"] = y_pred
        fold_errors["error"] = fold_errors["sales"] - fold_errors["y_pred"]
        fold_errors["abs_error"] = np.abs(fold_errors["error"])
        fold_errors["squared_error"] = fold_errors["error"] ** 2
        all_errors.append(fold_errors)

        print(
            f"{model_name} | Fold {fold} | "
            f"RMSLE={metrics['rmsle']:.6f} | "
            f"MAE={metrics['mae']:.3f} | "
            f"RMSE={metrics['rmse']:.3f} | "
            f"R2={metrics['r2']:.6f}"
        )

    metrics_df = pd.DataFrame(all_metrics)
    errors_df = pd.concat(all_errors, ignore_index=True)

    return metrics_df, errors_df