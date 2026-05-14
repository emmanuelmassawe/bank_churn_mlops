from prefect import flow, task 
import mlflow
import mlflow.sklearn
import pandas as pd 
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, f1_score

from config import DATA_PATH, TARGET_COLUMN, TEST_SIZE, RANDOM_STATE, COLUMNS_TO_DROP
from pipeline import build_pipeline

# ===== MLflow Settings (MUHIMU SANA!) =====
os.environ["MLFLOW_TRACKING_URI"] = "https://dagshub.com/emmanuelmassawe200/bank_churn_mlops.mlflow"
os.environ["MLFLOW_TRACKING_USERNAME"] = "emmanuelmassawe200"
os.environ["MLFLOW_TRACKING_PASSWORD"] = "2d1de8dba7efe82cbd12b1887e8ec78e2172fbaa"

mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])

@task 
def loading_data():
    print(f"📂 Loading data from {DATA_PATH}...")
    df = pd.read_csv(DATA_PATH)
    
    # Drop columns
    df = df.drop(columns=COLUMNS_TO_DROP)
    print(f"✅ Data shape after cleaning: {df.shape}")
    
    return df

@task 
def train_split(df):
    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN].astype(int)
    
    x_train, x_test, y_train, y_test = train_test_split(
        X, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y
    )
    
    print(f"✅ Train shape: {x_train.shape}, Test shape: {x_test.shape}")
    return x_train, x_test, y_train, y_test

@task 
def train_log(x_train, x_test, y_train, y_test):
    
    # Set experiment name
    mlflow.set_experiment("bank-churn-experiment")
    
    # Start MLflow run
    with mlflow.start_run() as run:
        print(f"🔬 MLflow Run ID: {run.info.run_id}")
        
        # Build pipeline
        pipe = build_pipeline()
        
        # Train
        pipe.fit(x_train, y_train)
        
        # Evaluate
        y_pred = pipe.predict(x_test)
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        
        print(report)
        print(f"✅ Accuracy: {acc:.4f}, F1 Score: {f1:.4f}")
        
        # Log params
        mlflow.log_param("model_type", "RandomForest")
        mlflow.log_param("test_size", TEST_SIZE)
        
        # Log metrics
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1_score", f1)
        
        # Log model (SAHIHI!)
        model_name = "bank-churn-model"  # ✅ Bila space
        mlflow.sklearn.log_model(
            sk_model=pipe,
            artifact_path="model",  # ✅ artifact_path, sio 'name'
            registered_model_name=model_name
        )
        
        print(f"✅ Model '{model_name}' registered successfully!")
        return pipe, acc

@flow(name="bank-churn-train-flow", log_prints=True)
def training_flow():
    print("🚀 Starting Training Flow...")
    
    # Step 1: Load data
    df = loading_data()
    
    # Step 2: Split data
    x_train, x_test, y_train, y_test = train_split(df)
    
    # Step 3: Train & log
    model, acc = train_log(x_train, x_test, y_train, y_test)
    
    print(f"✅ Training Complete! Final Accuracy: {acc:.4f}")

if __name__ == "__main__":
    training_flow()


 

    