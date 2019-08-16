from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.models import Variable

from airflow_ext.gfw import config as config_tools
from airflow_ext.gfw.models import DagFactory

PIPELINE = "pipe_vessels"


class VesselsPipelineDagFactory(DagFactory):
    def __init__(self, vessel_config, pipeline=PIPELINE, **kwargs):
        super(VesselsPipelineDagFactory, self).__init__(pipeline=pipeline, **kwargs)
        self.vessel_config = vessel_config

    def get_dag_id(self, prefix, vessel_pipe_name):
        return '{}.{}'.format(prefix, vessel_pipe_name)

    def build(self, dag_id):
        
        config = self.config
        config.update(self.vessel_config)

        with DAG(dag_id, schedule_interval=self.schedule_interval, default_args=self.default_args) as dag:
           
            config['date_range'] = ','.join(self.source_date_range())
            name = config['name']

            publish_vessel_info = BashOperator(
                task_id='publish_vessel_info_{}'.format(name),
                depends_on_past=True,
                bash_command='{docker_run} {docker_image} publish_vessel_info '
                '\'{bigquery_vessel_info_query}\' '
                '{project_id}:{temp_dataset} '
                '{temp_bucket} '
                '{elasticsearch_server_url} '
                '{elasticsearch_server_auth} '
                '{elasticsearch_index_alias} '
                '\'{elasticsearch_index_mappings}\''.format(**config)
            )

            aggregate_tracks = BashOperator(
                task_id='aggregate_tracks_{}'.format(name),
                pool='bigquery',
                depends_on_past=True,
                bash_command='{docker_run} {docker_image} aggregate_tracks '
                '{date_range} '
                '{bigquery_vessel_tracks_jinja_query} '
                '{project_id}:{target_dataset}.{bigquery_tracks} '.format(
                    **config)
            )

            publish_postgres_tracks = BashOperator(
                task_id='publish_postgres_tracks_{}'.format(name),
                depends_on_past=True,
                bash_command='{docker_run} {docker_image} publish_postgres_tracks '
                '{date_range} '
                '{project_id}:{target_dataset}.{bigquery_tracks} '
                '{project_id}:{temp_dataset} '
                '{temp_bucket} '
                '{postgres_instance} '
                '{postgres_connection_string} '
                '{postgres_table_tracks}'.format(**config)
            )

            check_source_existance = config.get('check_source_existance',None)
            if (check_source_existance is not None or not check_source_existance):
                dag >> aggregate_tracks
                dag >> publish_vessel_info
            else:
                source_sensors = self.source_table_sensors(dag)
                for sensor in source_sensors:
                    dag >> sensor
                    sensor >> aggregate_tracks
                    sensor >> publish_vessel_info
            aggregate_tracks >> publish_postgres_tracks

            return dag


modes=['daily','monthly']
vessels_configurations = config_tools.load_config(PIPELINE)['configurations']
for mode in modes:
    for vessels_configuration in vessels_configurations:
        dag_factory = VesselsPipelineDagFactory(vessels_configuration,schedule_interval='@{}'.format(mode))
        dag_id = dag_factory.get_dag_id(
                            '{}_{}'.format(PIPELINE, mode),
                            vessels_configuration['name']
                        )
        globals()[dag_id] = dag_factory.build(dag_id=dag_id)
