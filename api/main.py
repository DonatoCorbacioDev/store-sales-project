from __future__ import annotations

import json
import logging
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel


MODEL_DIR = Path("models")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Store Sales Forecasting API",
    version="1.0.0",
)


# Load model artifacts at startup
model = joblib.load(MODEL_DIR / "store_sales_lgbm.joblib")

logger.info("Model artifacts loaded successfully.")

with open(MODEL_DIR / "feature_list.json", "r", encoding="utf-8") as f:
    FEATURES = json.load(f)

with open(MODEL_DIR / "training_metadata.json", "r", encoding="utf-8") as f:
    MODEL_METADATA = json.load(f)


class ForecastRequest(BaseModel):
    store_nbr: int
    family: int
    onpromotion: int

    year: int
    month: int
    day: int
    dayofweek: int
    weekofyear: int
    is_weekend: int

    lag_1: float
    lag_7: float

    rolling_mean_7: float
    rolling_std_7: float
    rolling_mean_14: float

    trend_1_7: float
    promo_last_7: float


class ForecastResponse(BaseModel):
    prediction: float


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool


class ModelInfoResponse(BaseModel):
    model_name: str
    model_type: str
    target: str
    n_features: int
    n_training_rows: int
    train_start: str
    train_end: str
    features: list[str]


@app.get("/health", response_model=HealthResponse)
def health():
    return {
        "status": "ok",
        "model_loaded": model is not None,
    }


@app.get("/")
def root():
    return {
        "message": "Store Sales Forecasting API"
    }


@app.get("/model-info", response_model=ModelInfoResponse)
def model_info():
    return {
        "model_name": MODEL_METADATA.get("model_name"),
        "model_type": MODEL_METADATA.get("model_type"),
        "target": MODEL_METADATA.get("target"),
        "n_features": MODEL_METADATA.get("n_features"),
        "n_training_rows": MODEL_METADATA.get("n_training_rows"),
        "train_start": MODEL_METADATA.get("train_start"),
        "train_end": MODEL_METADATA.get("train_end"),
        "features": FEATURES,
    }


@app.post("/predict", response_model=ForecastResponse)
def predict(request: ForecastRequest):
    data = request.model_dump()

    X = pd.DataFrame([data])[FEATURES]

    prediction = model.predict(X)[0]
    prediction = max(float(prediction), 0.0)

    logger.info(
        "Prediction generated | store_nbr=%s | family=%s | prediction=%.4f",
        request.store_nbr,
        request.family,
        prediction,
    )

    return {
        "prediction": prediction
    }