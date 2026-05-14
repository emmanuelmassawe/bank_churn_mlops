"""
Configuration file - DagsHub na MLflow settings
"""
import os
import dagshub

# DagsHub credentials
DAGSHUB_USERNAME = "emmanuelmassawe200"
DAGSHUB_REPO_NAME = "bank_churn_mlops"
DAGSHUB_TOKEN = "2d1de8dba7efe82cbd12b1887e8ec78e2172fbaa"  # Token yako

# MLflow tracking URI
MLFLOW_TRACKING_URI = f"https://dagshub.com/{DAGSHUB_USERNAME}/{DAGSHUB_REPO_NAME}.mlflow"

# Set environment variables
os.environ["MLFLOW_TRACKING_URI"] = MLFLOW_TRACKING_URI
os.environ["MLFLOW_TRACKING_USERNAME"] = DAGSHUB_USERNAME
os.environ["MLFLOW_TRACKING_PASSWORD"] = DAGSHUB_TOKEN

# Data paths
DATA_PATH = "data/customer-churn-Records.csv"

# Model settings
TARGET_COLUMN = "Exited"
COLUMNS_TO_DROP = ["RowNumber", "CustomerId", "Surname", "Complain"]

# Train/test split
TEST_SIZE = 0.2
RANDOM_STATE = 42

print("✅ Config loaded successfully!")