# bank_churn_mlops
Complete MLOps System: Bank Customer Churn Prediction with Prefect, MLFlow, FastAPI, Docker &amp; CI/CD

# Bank Customer Churn Prediction — End-to-End MLOps Pipeline

[![CI/CD](https://img.shields.io/github/actions/workflow/status/emmanuelmassawe200/bank-churn-mlops/ci-cd.yml?branch=main&label=CI%2FCD&logo=github-actions)](https://github.com/emmanuelmassawe200/bank-churn-mlops/actions)
[![Docker Pulls](https://img.shields.io/docker/pulls/emmanuely2000/bank-churn-api?logo=docker)](https://hub.docker.com/r/emmanuely2000/bank-churn-api)
[![MLflow](https://img.shields.io/badge/MLflow-tracked-blue?logo=mlflow)](https://dagshub.com/emmanuelmassawe200/bank_churn_mlops)
[![Python](https://img.shields.io/badge/python-3.11-blue?logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> A production-grade MLOps system that predicts bank customer churn — built with the full lifecycle in mind: data versioning, experiment tracking, automated training, model serving, containerization, and CI/CD.

---

## Why I Built This

Churn prediction is one of those problems that sounds simple on paper but gets messy the moment you leave the notebook. I wanted to go beyond training a model and actually understand what it takes to build something that could run reliably in a real environment — versioned data, reproducible training, a real serving layer, and automated deployment.

This project covers the entire journey from raw CSV to a containerized REST API with a CI/CD pipeline pushing updated images to Docker Hub on every commit.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        TRAINING PIPELINE                            │
│                                                                     │
│   ┌──────────┐    ┌──────────────┐    ┌─────────────────────────┐  │
│   │  DagsHub │    │   Prefect    │    │  MLflow Model Registry  │  │
│   │  (DVC)   │───▶│  Training    │───▶│  (hosted on DagsHub)    │  │
│   │  Data    │    │  Flow        │    │                         │  │
│   └──────────┘    └──────────────┘    └────────────┬────────────┘  │
└──────────────────────────────────────────────────── │ ─────────────┘
                                                      │ Production model
┌─────────────────────────────────────────────────────▼───────────────┐
│                          SERVING LAYER                              │
│                                                                     │
│   ┌──────────────┐    ┌──────────────┐    ┌────────────────────┐   │
│   │   Browser /  │    │   FastAPI    │    │   Docker           │   │
│   │   Frontend   │◀───│   REST API   │◀───│   Container        │   │
│   │  (HTML/JS)   │    │   /predict   │    │   emmanuely2000/   │   │
│   └──────────────┘    └──────────────┘    │   bank-churn-api   │   │
│                                           └────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼─────────────────────────────────┐
│                          CI/CD PIPELINE                             │
│                                                                     │
│        GitHub Push ──▶ GitHub Actions ──▶ Build ──▶ Docker Hub     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Stack

| Layer | Tool | Purpose |
|---|---|---|
| Data versioning | DVC + DagsHub | Track dataset versions alongside code |
| Orchestration | Prefect | Run and monitor the training flow |
| ML framework | scikit-learn Pipeline | Bundle preprocessing + classifier into one artifact |
| Experiment tracking | MLflow on DagsHub | Log params, metrics, and register models |
| Serving | FastAPI + uvicorn | REST API for real-time predictions |
| UI | HTML / CSS / JS | Browser-based form to interact with the API |
| Containerization | Docker | Reproducible, portable runtime |
| Registry | Docker Hub | Versioned image storage |
| CI/CD | GitHub Actions | Automated test → build → push on every commit |

---

## Model Performance

**Algorithm:** Random Forest Classifier inside a scikit-learn Pipeline

The pipeline bundles preprocessing and classification as a single serializable object — one artifact logged, one artifact loaded, one artifact served.

| Metric | Score |
|---|---|
| Accuracy | 84.0% |
| F1-score (weighted) | 63.1% |


Top churn predictors:Age → Number of products → Balance → Geography → Active membership status



## Project Layout

```
bank-churn-mlops/
├── src/
│   ├── config.py          # MLflow + DagsHub config
│   ├── pipeline.py        # sklearn Pipeline definition
│   ├── train_flow.py      # Prefect training flow
│   └── evaluate.py        # Metric helpers
├── api/
│   └── app.py             # FastAPI application
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Quick Start

**Run with Docker**

```bash
docker pull emmanuely2000/bank-churn-api:latest

docker run -d -p 8000:8000 \
  -e MLFLOW_TRACKING_URI=<your-mlflow-uri> \
  -e MLFLOW_TRACKING_USERNAME=<username> \
  -e MLFLOW_TRACKING_PASSWORD=<password> \
  emmanuely2000/bank-churn-api:latest
```

API docs available at [http://localhost:8000/docs](http://localhost:8000/docs)

**Run locally**

```bash
git clone https://github.com/emmanuelmassawe200/bank-churn-mlops.git
cd bank-churn-mlops
pip install -r requirements.txt
python api/app.py
```

**Retrain the model**

```bash
python src/train_flow.py
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API info and status |
| GET | `/health` | Health check and model status |
| POST | `/predict` | Predict churn for one or more customers |
| GET | `/docs` | Interactive Swagger UI |

---

## What I Ran Into

Building this end-to-end exposed a few things that tutorials don't usually warn you about.

**scikit-learn version mismatch** — I trained with scikit-learn 1.8.0 but the Docker base image pulled 1.3.2. The model would load but predictions failed on some estimators. The fix was removing pinned versions from `requirements.txt` and letting pip resolve compatible versions. Lesson: version constraints in ML serving are more fragile than they look.

**Docker and secrets** — Early on I put MLflow credentials directly in the Dockerfile. That bakes them into the image layers and exposes them to anyone who pulls the image. Switched to runtime environment variables via `docker run -e`, which keeps the image clean and shareable.

**CORS between frontend and API** — Opening `index.html` directly from the filesystem uses `file://` as the origin, which browsers block when making requests to `localhost`. Added `CORSMiddleware` to FastAPI. Simple fix once you know what's causing it.

**MLflow staging confusion** — The API was configured to load the model by stage (`Production`), but the model hadn't been promoted yet and sat at stage `None`. This gave a `RESOURCE_DOES_NOT_EXIST` error with no helpful context. Switched to loading by version number while building out the promotion workflow.

---

## What I'd Add Next

- Model drift detection with Evidently — compare incoming prediction distributions against training data over time
- Scheduled retraining via a Prefect deployment with a weekly cron trigger
- SHAP values on `/predict` responses so the business can see what drove each prediction
- Cloud deployment on GCP Cloud Run or AWS ECS for a public endpoint

---

## Links

- [Docker Hub Image](https://hub.docker.com/r/emmanuely2000/bank-churn-api)
- [MLflow Experiments on DagsHub](https://dagshub.com/emmanuelmassawe200/bank_churn_mlops)

---

## Author

**Emmanuel Massawe**  
[GitHub](https://github.com/emmanuelmassawe200) · [LinkedIn](https://linkedin.com/in/emmanuel-massawe) · [Docker Hub](https://hub.docker.com/u/emmanuely2000)

---

*Built as a portfolio project to demonstrate the full MLOps lifecycle — not just model training.*
