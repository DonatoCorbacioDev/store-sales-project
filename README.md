# 📊 Store Sales Forecasting — Production-Oriented Retail Forecasting System

Production-oriented retail forecasting project based on the Kaggle *Store Sales Time Series Forecasting* dataset.

The objective is not only to improve predictive accuracy, but to simulate how a forecasting system should be developed, validated, evaluated, served and monitored in a real-world ML environment.

The project progressively evolves from baseline forecasting to business-aware evaluation, trust scoring, monitoring-oriented forecasting governance and containerized ML serving.

---

# 🚀 Project Overview

This project was designed as a realistic forecasting workflow rather than a pure Kaggle competition solution.

The system focuses on:

* robust temporal validation
* reproducible experimentation
* operational risk analysis
* trust-aware forecasting
* monitoring and drift detection
* production-oriented ML reasoning
* containerized inference serving
* CI-based Docker validation

The final goal is not simply to predict sales.

The goal is to build a forecasting system that can be:

* validated correctly
* interpreted operationally
* served through an API
* monitored over time
* trusted conditionally
* improved where business risk is highest

---

# 🧠 Architecture

```text
Raw retail data
        ↓
Feature engineering
        ↓
Temporal validation
        ↓
LightGBM / AutoGluon models
        ↓
MLflow experiment tracking
        ↓
Business-aware evaluation
        ↓
Forecast trust scoring
        ↓
Monitoring & drift analysis
        ↓
Saved model artifact
        ↓
FastAPI inference service
        ↓
Docker containerization
        ↓
GitHub Actions CI
```

---

# 📦 Dataset

* Source: Kaggle — Store Sales Time Series Forecasting
* Granularity: daily sales per `(store_nbr, family)`
* Period: 2013 → 2017
* Dataset size: ~3M rows

Main datasets used:

* `train.csv`
* `test.csv`

Additional datasets available for future improvements:

* `oil.csv`
* `transactions.csv`
* `holidays_events.csv`
* `stores.csv`

Raw dataset files are not committed to the repository. They should be downloaded from Kaggle and placed inside the `data/` directory.

---

# ⚙️ Tech Stack

* Python
* Pandas / NumPy
* LightGBM
* Scikit-learn
* MLflow
* AutoGluon
* Matplotlib
* Jupyter Notebook
* FastAPI
* Pydantic
* Docker
* Docker Compose
* GitHub Actions

---

# 📓 Notebook Roadmap

## Core Forecasting Pipeline

* NB1 — Baseline Model
* NB2 — Baseline Error Analysis
* NB3 — Advanced Feature Engineering
* NB4 — MLflow Experiment Tracking
* NB5 — Walk-Forward Cross-Validation
* NB6 — Final Candidate Retraining
* NB7 — Full CV Error Analysis
* NB8 — Targeted Promo & High-Sales Diagnostics

## AutoML & Benchmarking

* NB9 — AutoGluon Benchmark
* NB10 — AutoGluon Model Inspection
* NB11 — AutoGluon Extended Budget

## Business & Operational Forecasting

* NB12 — Business-Aware Forecast Evaluation
* NB13 — Business Error Diagnosis & Action Plan
* NB14 — Forecast Trust Scoring & Decision Framework
* NB15 — Forecast Monitoring & Drift Strategy

## Time-Series Methodology Comparison

* NB16 — AutoGluon TimeSeries vs Tabular Forecasting

---

# 📈 Key Results

## Modeling Performance

| Model                           | RMSLE         |
| ------------------------------- | ------------- |
| Baseline (NB1)                  | ~0.78         |
| Validated manual pipeline (NB5) | ~0.60 ± 0.015 |
| AutoGluon benchmark (NB9)       | ~0.476        |

## Operational Findings

* Promotions are the primary driver of costly forecast failures
* Underforecast is the most expensive residual error
* Forecast risk is concentrated in a small number of store/family pockets
* High-sales periods remain the most operationally fragile scenarios

## Trust Scoring Results

| Forecast Tier           | Share  |
| ----------------------- | ------ |
| Safe forecasts          | 33.72% |
| Manual review forecasts | 50.92% |
| Risky forecasts         | 15.36% |

## Monitoring Findings

* Stable forecast behavior: ~75%
* Drift windows are observable and monitorable
* Promotions remain the main driver of degradation

---

# 📊 Validation Strategy

The project uses walk-forward cross-validation with expanding windows.

Validation setup:

* 4 folds
* 28-day validation windows
* past-only training
* no temporal leakage

This validation strategy better simulates real-world forecasting conditions compared to a single random split.

---

# 🧩 Repository Structure

```text
store-sales-project/
│
├── api/
│   ├── main.py
│   ├── config.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── data/
├── models/
├── notebooks-tabular/
├── notebooks-time-series/
├── src/
│   ├── features.py
│   ├── split.py
│   ├── metrics.py
│   ├── tracking.py
│   ├── evaluation.py
│   ├── automl.py
│   ├── train.py
│   ├── predict.py
│   └── error_analysis.py
│
├── artifacts/
├── notes/
├── .github/workflows/
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# 🐳 Docker & FastAPI Serving

The project includes a containerized FastAPI inference service.

Current serving workflow:

```text
Training pipeline
        ↓
Saved model artifact (.joblib)
        ↓
FastAPI inference API
        ↓
Docker container
        ↓
Docker Compose orchestration
```

API features:

* `/health` endpoint
* `/model-info` metadata endpoint
* `/predict` inference endpoint
* Swagger UI documentation
* typed Pydantic request/response schemas
* basic API logging
* Dockerized serving
* mounted model artifacts
* production-oriented API structure

Run locally:

```bash
docker compose up --build
```

Open:

```text
http://localhost:8000/docs
```

---

# 🔌 API Usage

## Health Check

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "model_loaded": true
}
```

---

## Model Metadata

```bash
curl http://localhost:8000/model-info
```

This endpoint returns metadata about the loaded model artifact, including:

* model name
* model type
* target variable
* number of features
* training date range
* feature list

---

## Forecast Prediction

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
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
    "promo_last_7": 0.0
  }'
```

Example response:

```json
{
  "prediction": 4.802244603023583
}
```

---

# ⚙️ CI/CD

The repository includes a GitHub Actions workflow for Docker build validation.

Current CI pipeline:

* Docker image build validation
* API container build verification
* production-oriented repository structure validation

This ensures that the API container remains buildable after each push to the main branch.

---

# 🔄 Current Status

✅ Baseline forecasting pipeline completed
✅ Walk-forward validation completed
✅ MLflow experiment tracking completed
✅ AutoML benchmarking completed
✅ Business-aware evaluation completed
✅ Forecast trust scoring completed
✅ Monitoring & drift strategy completed
✅ Reusable training script completed
✅ Reusable prediction script completed
✅ Dockerized FastAPI inference service completed
✅ GitHub Actions Docker CI completed
🔄 Further production hardening in progress

---

# ▶️ How to Run

## Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run notebooks

Start from:

```text
notebooks-tabular/nb1_baseline_correct_pipeline.ipynb
```

Then continue sequentially through the forecasting workflow.

---

## Train the forecasting model

```bash
python3 -m src.train --data-dir data --model-dir models
```

This creates the model artifacts inside:

```text
models/
```

---

## Run local prediction script

```bash
python3 -m src.predict
```

---

## Run FastAPI locally

```bash
uvicorn api.main:app --reload
```

---

## Run with Docker Compose

```bash
docker compose up --build
```

---

# 🧪 MLflow Tracking

Launch MLflow UI:

```bash
mlflow ui --backend-store-uri ./mlruns
```

Open:

```text
http://127.0.0.1:5000
```

---

# 🏭 Production-Oriented Design

The project simulates a production-oriented ML workflow:

* strict temporal validation
* reusable feature engineering
* experiment tracking
* business-aware evaluation
* operational risk analysis
* trust-aware forecasting
* monitoring and drift strategy
* model artifact persistence
* containerized inference serving
* API metadata endpoint
* typed request/response schemas
* CI-oriented repository structure

The project should be considered a production-oriented forecasting prototype rather than a fully deployed production system.

---

# 🔮 Planned ML Engineering Extensions

Planned next steps:

* model registry integration
* artifact versioning
* retraining orchestration
* monitoring dashboard
* advanced transformer forecasting experiments
* DST-aware energy forecasting experiments
* Moirai / foundation-model experimentation

---

# ⚠️ Limitations

* limited modeling of external regressors
* no explicit hierarchical forecasting
* promotions remain difficult to model
* extreme demand spikes are still challenging
* no distributed training
* no real cloud deployment yet
* model artifacts are generated locally and mounted into the API container

---

# 🧠 Key Takeaways

* Forecast quality should not be evaluated only by RMSE/RMSLE
* The best benchmark model is not always the best production candidate
* Forecasts should be evaluated in terms of business impact and operational risk
* Forecast outputs should become trust-aware decision signals
* Forecast systems should be monitored continuously after deployment
* ML models become more useful when they are served, versioned and monitored as software systems

---

# 🧾 Final Note

This project demonstrates not only how forecasting models can be trained, but how forecasting systems can be structured, validated, served and monitored in realistic ML environments.

The final output is not simply a sales prediction model.

It is a production-oriented forecasting workflow including:

* robust validation
* operational risk analysis
* trust-aware evaluation
* monitoring and drift governance
* containerized inference serving
* CI-oriented deployment foundations
