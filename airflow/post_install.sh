#!/bin/bash

THIS_SCRIPT_DIR="$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )"

python $AIRFLOW_HOME/utils/set_default_variables.py \
    --force docker_image=$1 \
    pipe_vessels \
    dag_install_path="${THIS_SCRIPT_DIR}" \
    docker_run="{{ var.value.DOCKER_RUN }}" \
    project_id="{{ var.value.PROJECT_ID }}" \
    temp_bucket="{{ var.value.TEMP_BUCKET }}"  \
    pipeline_bucket="{{ var.value.PIPELINE_BUCKET }}" \
    pipeline_dataset="{{ var.value.PIPELINE_DATASET }}" \
    temp_dataset="{{ var.value.TEMP_DATASET }}" \
    bigquery_tracks="tracks" \


echo "Installation Complete"
