from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
from lightgbm import LGBMRegressor

from src.features import add_baseline_features, add_advanced_features, encode_family

SEED = 42
TARGET = "sales"


def add_calendar_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["dayofweek"] = df["date"].dt.dayofweek
    df["weekofyear"] = df["date"].dt.isocalendar().week.astype(int)
    df["is_weekend"] = df["dayofweek"].isin([5, 6]).astype(int)
    return df


def train_final_model(data_dir: Path, model_dir: Path) -> None:
    model_dir.mkdir(parents=True, exist_ok=True)

    train_path = data_dir / "train.csv"
    test_path = data_dir / "test.csv"

    train = pd.read_csv(train_path, parse_dates=["date"])
    test = pd.read_csv(test_path, parse_dates=["date"])

    train = train.sort_values(["store_nbr", "family", "date"]).copy()
    test = test.sort_values(["store_nbr", "family", "date"]).copy()

    train = add_calendar_features(train)
    test = add_calendar_features(test)

    train = add_baseline_features(train)
    train = add_advanced_features(train)
    train = train.dropna().copy()

    train, test, family_mapping = encode_family(train, test)

    features = [
        "store_nbr",
        "family",
        "onpromotion",
        "year",
        "month",
        "day",
        "dayofweek",
        "weekofyear",
        "is_weekend",
        "lag_1",
        "lag_7",
        "rolling_mean_7",
        "rolling_std_7",
        "rolling_mean_14",
        "trend_1_7",
        "promo_last_7",
    ]

    X_train = train[features]
    y_train = train[TARGET]

    model = LGBMRegressor(
        n_estimators=300,
        learning_rate=0.05,
        num_leaves=31,
        random_state=SEED,
        n_jobs=-1,
    )

    model.fit(X_train, y_train)

    joblib.dump(model, model_dir / "store_sales_lgbm.joblib")

    with open(model_dir / "feature_list.json", "w", encoding="utf-8") as f:
        json.dump(features, f, indent=2)

    with open(model_dir / "family_mapping.json", "w", encoding="utf-8") as f:
        json.dump(family_mapping, f, indent=2)

    metadata = {
        "model_name": "store_sales_lgbm",
        "model_type": "LGBMRegressor",
        "target": TARGET,
        "n_features": len(features),
        "n_training_rows": int(len(train)),
        "train_start": str(train["date"].min()),
        "train_end": str(train["date"].max()),
        "seed": SEED,
    }

    with open(model_dir / "training_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print("Training completed.")
    print(f"Model saved to: {model_dir / 'store_sales_lgbm.joblib'}")
    print(f"Training rows: {len(train)}")
    print(f"Features: {len(features)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train final Store Sales LightGBM model.")
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--model-dir", type=Path, default=Path("models"))
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    train_final_model(data_dir=args.data_dir, model_dir=args.model_dir)