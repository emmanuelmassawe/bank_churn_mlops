import pandas as pd 
from sklearn.preprocessing import StandardScaler, LabelEncoder,OneHotEncoder
from imblearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import RobustScaler
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import SMOTE

# Columns za aina tofauti
NUMERIC_FEATURES = [
    "CreditScore", "Age", "Tenure", "Balance",
    "NumOfProducts", "HasCrCard", "IsActiveMember",
    "EstimatedSalary", "Satisfaction Score", "Point Earned"
]

CATEGORICAL_FEATURES = [
    "Geography", "Gender", "Card Type"
]

def build_pipeline():

    # Numeric pipeline
    numeric_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", RobustScaler())
        
    ])

    # Categorical pipeline
    categorical_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer(transformers=[
        ('num', numeric_transformer,NUMERIC_FEATURES),
        ('cat', categorical_transformer,CATEGORICAL_FEATURES)
    ])
    pipeline = Pipeline( steps = [
        ('preprocessor',preprocessor),
        ('smote', SMOTE(random_state = 42)),
        ('classifier', RandomForestClassifier(
            n_estimators=  100,
            n_jobs= -1,
            max_depth= 10,
            max_samples= 0.8,
            class_weight= 'balanced'

        ))
    ])

    return pipeline

if __name__ == "__main__":
    pipe = build_pipeline()
    print(" the pipeline is successful built")
    print(pipe)
