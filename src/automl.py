from __future__ import annotations

import shutil
import time
from pathlib import Path

import numpy as np
import pandas as pd
from autogluon.tabular import TabularPredictor

from src.metrics import evaluate_regression


def evaluate_autogluon(
    df: pd.DataFrame,
    features: list[str],
    folds: list[dict],
    model_dir: Path,
    time_limit: int,
    presets: str,
    target: str = "sales",
) -> tuple[pd.DataFrame, list[pd.DataFrame]]:
    """
    Train and evaluate AutoGluon Tabular on walk-forward folds.

    Returns:
        - metrics per fold
        - AutoGluon leaderboards per fold
    """
    metrics_rows = []
    leaderboards = []

    model_dir.mkdir(parents=True, exist_ok=True)

    for fold_info in folds:
        fold = fold_info["fold"]

        print("\n" + "=" * 80)
        print(f"Starting AutoGluon benchmark - Fold {fold}")
        print("=" * 80)

        train_fold = df[df["date"] <= fold_info["train_end"]].copy()
        val_fold = df[
            (df["date"] >= fold_info["val_start"])
            & (df["date"] <= fold_info["val_end"])
        ].copy()

        train_ag = train_fold[features + [target]].copy()
        X_val = val_fold[features].copy()
        y_val = val_fold[target]

        fold_model_path = model_dir / f"fold_{fold}"

        if fold_model_path.exists():
            print("Removing previous AutoGluon model folder:", fold_model_path)
            shutil.rmtree(fold_model_path)

        start_time = time.time()

        predictor = TabularPredictor(
            label=target,
            problem_type="regression",
            eval_metric="root_mean_squared_error",
            path=str(fold_model_path),
            verbosity=2,
        ).fit(
            train_data=train_ag,
            presets=presets,
            time_limit=time_limit,
        )

        train_time_sec = time.time() - start_time

        pred_start_time = time.time()
        y_pred = predictor.predict(X_val).values
        inference_time_sec = time.time() - pred_start_time

        y_pred = np.clip(y_pred, 0, None)

        metrics = evaluate_regression(y_val, y_pred)

        leaderboard = predictor.leaderboard(silent=True)
        leaderboard["fold"] = fold
        leaderboards.append(leaderboard)

        best_model_row = leaderboard.sort_values("score_val", ascending=False).iloc[0]

        row = {
            "fold": fold,
            "train_end": fold_info["train_end"],
            "val_start": fold_info["val_start"],
            "val_end": fold_info["val_end"],
            "n_train": len(train_fold),
            "n_val": len(val_fold),
            "train_time_sec": train_time_sec,
            "inference_time_sec": inference_time_sec,
            "autogluon_time_limit": time_limit,
            "autogluon_presets": presets,
            "best_model": best_model_row["model"],
            "best_model_score_val": best_model_row["score_val"],
            "best_model_fit_time": best_model_row["fit_time"],
            "best_model_pred_time_val": best_model_row["pred_time_val"],
            **metrics,
        }

        metrics_rows.append(row)

        print(
            f"AutoGluon | Fold {fold} | "
            f"Best={best_model_row['model']} | "
            f"RMSLE={metrics['rmsle']:.6f} | "
            f"MAE={metrics['mae']:.3f} | "
            f"RMSE={metrics['rmse']:.3f} | "
            f"R2={metrics['r2']:.6f} | "
            f"Train time={train_time_sec:.1f}s"
        )

    return pd.DataFrame(metrics_rows), leaderboards