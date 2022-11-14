# Setting up mlflow
## Install mlflow:

    pip install mlflow

## Open the UI in the localhost:

    mlflow ui --backend-store-uri directory_to_the_folder/mlruns

In case the port is already in use, we can Kill the PID using that port:
* Get the PIDs using s given port, in our example it is 5000

      sudo lsof -i :5000 

* Kill each PID:
  
      sudo kill -9 27566

![Alt text](images/kill_PID.png "KILL-PID-ON_MAC")

# Setting up mlflow to use postgres database: Database Tracking, Minio Artifact Storage
In this solution, the mlflow uses a PostgreSQL DB as the tracking URI and Minio as the artifact URI.
![Alt text](images/mlflow-functional-process.drawio.png "mlflow functional process")

## Install brew
    git -C /usr/local/Homebrew/Library/Taps/homebrew/homebrew-core fetch --unshallow

## Install postgresql
    brew install postgresql

## To restart postgresql@14 after an upgrade:
    brew services restart postgresql@14

## Create a DB User “ml_user” with Password “1234” (in psql command line)
We need to specify the default user, in case there is a conflict or the default username is wrong.
open a terminal then write:

    psql postgres --u postgres

    CREATE ROLE ml_user WITH LOGIN PASSWORD '1234';


Create Database:
    
    CREATE DATABASE mlflow_db;

Grant the User access to the Database:

    GRANT ALL PRIVILEGES ON DATABASE mlflow_db TO ml_user;


## configure MINIO cloud artifact storage: compatible with S3.
Open a terminal or exit from the sql mode then:

Install Minio:

    brew install minio/stable/minio

Make a Data Folder for Minio:

    mkdir /Users/user/Downloads/data

Open Minio UI: The default port for minio is 9000, but we can change it by specifying --address. 

    minio server /Users/user/Downloads/data --address ":9001"

# Open the mlflow ui using the postgres database backend
Before opening the ui we need to check the port if it is already in use. If so we need to kill the PIDs.
Set the S3 endpoint URL with the URL returned when we spun up our Minio UI.
We need to export all the variables below: 
* MLFLOW_TRACKING_URI, 
* MLFLOW_S3_ENDPOINT_URL,
* AWS_ACCESS_KEY_ID, 
* AWS_SECRET_ACCESS_KEY.

The artifact section (getting data from minio) of the mlflow ui will work only when we execute these lines:
![img.png](images/mlflow_ui_artifact.png)

    export MLFLOW_TRACKING_URI=postgresql+psycopg2://ml_user:1234@localhost/mlflow_db
    export MLFLOW_S3_ENDPOINT_URL=http://10.0.0.148:9001
    export AWS_ACCESS_KEY_ID=minioadmin
    export AWS_SECRET_ACCESS_KEY=minioadmin
    mlflow ui --backend-store-uri 'postgresql+psycopg2://ml_user:1234@localhost/mlflow_db'


![Alt text](images/mlflow_ui_with_minio.png "mlflow functional process")

## Using mlflow as a Docker container
Note: You can use that solution only if you have a professional version of the pycharm IDE.

It is possible to create a docker image having the mlflow environment and use it inside an IDE such as pycharm.
This solution has some advantages in terms of scalability compared to using a virtual environment.
The idea is simple, first of all you need to install few packages in your local virtual envoroment.
   
    conda install -c conda-forge mlflow=1.8.0

    bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"

    brew install git

    git clone https://github.com/Noodle-ai/mlflow_part2_dockerEnv.git

### Build an Image from the Dockerfile

    docker image build -t mlflow_image .

### Build a Container from the Image
    docker run -d -P --mount type=bind,source=$(pwd),target=/home/dockeruser --name mlflow_container mlflow_image

Once the container is built and running we switch to the IDE side.
We need to create a new interpreter and select Docker as option:
![img.png](images/pycharm_interpreter_docker_option.png)
Create a new server:
![img.png](images/docker_pycharm_interpreter_new_server.png)
Select Docker image:
![img.png](images/docker_pycharm_select_docker_image.png)
In that case, your python project will use the remote interpreter. The one that is already defined based on the docker container.



