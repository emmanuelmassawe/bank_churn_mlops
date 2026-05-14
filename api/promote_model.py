import mlflow
import os

os.environ['MLFLOW_TRACKING_URI'] = 'https://dagshub.com/emmanuelmassawe200/bank_churn_mlops.mlflow'
os.environ['MLFLOW_TRACKING_USERNAME'] = 'emmanuelmassawe200'
os.environ['MLFLOW_TRACKING_PASSWORD'] = '2d1de8dba7efe82cbd12b1887e8ec78e2172fbaa'

from mlflow.tracking import MlflowClient

client = MlflowClient()
client.transition_model_version_stage(
    name='bank-churn-model',
    version=1,
    stage='Production'
)
print('✅ Model promoted to Production!')