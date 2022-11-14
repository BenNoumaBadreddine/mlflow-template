from configs.database_configs import MLFLOW_DB_CONFIG
from databases_schema.mlflow_db_schema import Experiment
from utils.general_utils import db_instances_to_dataframe
from dbconnections.databases_connection import get_db_connection

MLFLOW_DB_CONNECTION = get_db_connection(MLFLOW_DB_CONFIG)
with MLFLOW_DB_CONNECTION.session as session:
    query = session.query(Experiment.experiment_id).all()
df = db_instances_to_dataframe(query)
print(df)

