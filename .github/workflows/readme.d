# 🏦 Bank Churn Prediction MLOps System

![CI/CD](https://github.com/YOUR-USERNAME/bank-churn-mlops/workflows/🏦%20MLOps%20Pipeline/badge.svg)
![Docker](https://img.shields.io/docker/automated/emmanuely2000/bank-churn-api)

> Complete MLOps pipeline for bank customer churn prediction with AI

## 🚀 Quick Start

```bash
# Pull & run the latest version
docker pull emmanuely2000/bank-churn-api:latest

docker run -d -p 8000:8000 \
  -e MLFLOW_TRACKING_URI=<your-mlflow-uri> \
  -e MLFLOW_TRACKING_USERNAME=<username> \
  -e MLFLOW_TRACKING_PASSWORD=<password> \
  --name churn-api \
  emmanuely2000/bank-churn-api:latest

# Open API docs
open http://localhost:8000/docs