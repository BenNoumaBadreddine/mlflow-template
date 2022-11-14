import mlflow
import os
from sklearn import linear_model

from mlflow_utils.mlflow_utils_functions import set_experiment, print_mlflow_experiment_config


# use the Minio plateform as an artifact uri you need to open a terminal and execute:
# minio server /Users/badr/Downloads/data --address ":9001"

experiment_name = 'demo'
artifact_location = os.environ.get('MLFLOW_ARTIFACT_LOCATION')
tracking_uri = os.environ.get('MLFLOW_TRACKING_URI')
print(tracking_uri, artifact_location)
mlflow.set_tracking_uri(tracking_uri)
experiment_id = set_experiment(experiment_name, artifact_location)
experiment = mlflow.get_experiment(experiment_id)
print_mlflow_experiment_config(experiment)
mlflow.set_experiment(experiment_name)
# Auto log all the parameters, metrics, and artifacts
mlflow.tensorflow.autolog()

tags = {"engineering": "ML Platform", "engineering_remote": "ML Platform"}
description = 'This is a machine learning project using sklearn linear regression algorithm'
with mlflow.start_run(run_name="sklearn linear regression", description=description):
    reg = linear_model.LinearRegression()
    reg.fit([[0, 0], [1, 1], [2, 2]], [0, 1, 2])
    mlflow.sklearn.log_model(reg, "model")
    mlflow.log_param("input_vector_dimension", 2)
    mlflow.log_metric("rmse", 0.002)  # not real value just for illustration purposes (how to log metric in mlflow).
    # Log an artifact (output file)
    with open("output.txt", "w") as f:
        f.write("Hello world!")
    mlflow.log_artifact("output.txt")
    mlflow.set_tags(tags)
