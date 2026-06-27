import os 
import mlflow.pyfunc
import pandas as pd
from fastapi import HTTPException, FastAPI


app = FastAPI(
    title ="bank-churn-mlops",
    description = "predict if the bank will churn or not",
    version = "1.0.0" )

# app.py - tumia dotenv
from dotenv import load_dotenv
load_dotenv()
os.environ["MLFLOW_TRACKING_USERNAME"] = os.getenv("MLFLOW_TRACKING_USERNAME")
os.environ["MLFLOW_TRACKING_PASSWORD"] = os.getenv("MLFLOW_TRACKING_PASSWORD")

mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])

from pydantic import BaseModel
from typing import List 

class CustomerData(BaseModel):
    CreditScore: float
    Geography: str
    Gender: str
    Age: float
    Tenure: float
    Balance: float
    NumOfProducts: float
    HasCrCard: float
    IsActiveMember: float
    EstimatedSalary: float
    Satisfaction_Score: float
    Card_Type: str
    Point_Earned: float

class PredictionRequest(BaseModel):
    data: List[CustomerData]

class PredictionResponse(BaseModel):
    status: str
    predictions: List[dict]


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

MODEL_NAME = "bank-churn-model"
MODEL_VERSION  = "1"

print(f" Loading model {MODEL_NAME}/{MODEL_VERSION}...")

model = mlflow.pyfunc.load_model(f"models:/{MODEL_NAME}/{MODEL_VERSION}")

@app.get("/")
def home():
    return {
        "message": "🏦 Bank Churn Prediction API",
        "status": "running ✅",
        "docs": "Go to /docs for Swagger UI"
    }

@app.get("/health")
def health():
    return {
        "status": "ok ✅",
        "model_loaded": model is not None,
        "model_name": MODEL_NAME,
        "model_stage": MODEL_VERSION
    }

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please check MLflow connection."
        )
    try:
        # Convert to DataFrame
        input_data = [customer.dict() for customer in request.data]
        input_df = pd.DataFrame(input_data)

        # Rename columns kufikia sklearn pipeline
        input_df = input_df.rename(columns={
            "Satisfaction_Score": "Satisfaction Score",
            "Card_Type": "Card Type",
            "Point_Earned": "Point Earned"
        })

        # Predict
        predictions = model.predict(input_df)

        # Format results
        results = []
        for i, pred in enumerate(predictions):
            results.append({
                "customer_index": i + 1,
                "prediction": int(pred),
                "result": "🚨 Will Churn" if pred == 1 else "✅ Will Stay",
            })

        return {
            "status": "success",
            "predictions": results
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)
