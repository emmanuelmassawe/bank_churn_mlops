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