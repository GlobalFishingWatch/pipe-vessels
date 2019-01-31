from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.models import Variable
from pipe_tools.airflow.models import DagFactory

PIPELINE = "pipe_vessels"


class PipelineDagFactory(DagFactory):
    def __init__(self, pipeline=PIPELINE, **kwargs):
        super(PipelineDagFactory, self).__init__(pipeline=pipeline, **kwargs)

    def build(self, dag_id):
        config = self.config

        with DAG(dag_id, schedule_interval=self.schedule_interval, default_args=self.default_args) as dag:
            source_sensors = self.source_table_sensors(dag)

            aggregate_tracks = BashOperator(
                task_id='aggregate_tracks',
                pool='bigquery',
                bash_command='{docker_run} {docker_image} aggregate_tracks '
                '{project_id}:{source_dataset}.{source_table} '
                '{project_id}:{pipeline_dataset}.{bigquery_tracks} '.format(
                    **config)
            )

            publish_postgres_tracks = BashOperator(
                task_id='publish_postgres_tracks',
                bash_command='{docker_run} {docker_image} publish_postgres_tracks '
                '{project_id}:{pipeline_dataset}.{bigquery_tracks} '
                '{temp_bucket} '
                '{postgres_instance} '
                '{postgres_connection_string} '
                '{postgres_table_tracks}'.format(**config)
            )

            publish_postgres_vessels = BashOperator(
                task_id='publish_postgres_vessels',
                bash_command='{docker_run} {docker_image} publish_postgres_vessels '
                '{project_id}:{source_dataset}.{bigquery_segment_vessel} '
                '{temp_bucket} '
                '{postgres_instance} '
                '{postgres_connection_string} '
                '{postgres_table_vessels}'.format(**config)
            )

            for sensor in source_sensors:
                dag >> sensor >> aggregate_tracks >> (
                    publish_postgres_tracks, publish_postgres_vessels)

            return dag


vessels_daily = PipelineDagFactory().build('pipe_vessels_daily')
