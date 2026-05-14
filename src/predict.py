from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd


def load_artifacts(model_dir: Path):
    model = joblib.load(model_dir / "store_sales_lgbm.joblib")

    with open(model_dir / "feature_list.json", "r", encoding="utf-8") as f:
        features = json.load(f)

    with open(model_dir / "training_metadata.json", "r", encoding="utf-8") as f:
        metadata = json.load(f)

    return model, features, metadata


def predict_sample(model_dir: Path = Path("models")) -> float:
    model, features, metadata = load_artifacts(model_dir)

    sample = {
        "store_nbr": 1,
        "family": 0,
        "onpromotion": 0,
        "year": 2017,
        "month": 8,
        "day": 16,
        "dayofweek": 2,
        "weekofyear": 33,
        "is_weekend": 0,
        "lag_1": 7.0,
        "lag_7": 5.0,
        "rolling_mean_7": 6.2,
        "rolling_std_7": 1.4,
        "rolling_mean_14": 5.8,
        "trend_1_7": 2.0,
        "promo_last_7": 0.0,
    }

    X = pd.DataFrame([sample])[features]
    prediction = model.predict(X)[0]
    prediction = max(float(prediction), 0.0)

    print("Model:", metadata["model_name"])
    print("Prediction:", prediction)

    return prediction


if __name__ == "__main__":
    predict_sample()