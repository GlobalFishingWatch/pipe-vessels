from airflow import DAG
from airflow.models import Variable
from airflow.models import Variable
from airflow.operators.bash_operator import BashOperator

from airflow_ext.gfw import config as config_tools
from airflow_ext.gfw.models import DagFactory
from airflow_ext.gfw.operators.helper.flexible_operator import FlexibleOperator

from datetime import datetime, timedelta


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
            flexible_operator_var = Variable.get('FLEXIBLE_OPERATOR')

            publish_vessel_info_params = {
                'task_id':'publish_vessel_info_{}'.format(name),
                'depends_on_past':True,
                'pool':'k8operators_limit' if flexible_operator_var == 'kubernetes' else 'bigquery',
                'docker_run':'{docker_run}'.format(**config),
                'image':'{docker_image}'.format(**config),
                'name':'pipe-vessels-publish-vessel-info-{}'.format(name),
                'dag':dag,
                'arguments':['publish_vessel_info',
                             '{bigquery_vessel_info_query}'.format(**config),
                             '{project_id}:{temp_dataset}'.format(**config),
                             '{temp_bucket}'.format(**config),
                             '{elasticsearch_server_url}'.format(**config),
                             '{elasticsearch_server_auth}'.format(**config),
                             '{elasticsearch_index_alias}'.format(**config),
                             '{elasticsearch_index_mappings}'.format(**config)]
            }
            publish_vessel_info = FlexibleOperator(publish_vessel_info_params).build_operator(flexible_operator_var)

            aggregate_tracks_params = {
                'task_id':'aggregate_tracks_{}'.format(name),
                'depends_on_past':True,
                'pool':'k8operators_limit' if flexible_operator_var == 'kubernetes' else 'bigquery',
                'docker_run':'{docker_run}'.format(**config),
                'image':'{docker_image}'.format(**config),
                'name':'pipe-vessels-aggregate-tracks-{}'.format(name),
                'dag':dag,
                'arguments':['aggregate_tracks',
                             '{date_range}'.format(**config),
                             '{bigquery_vessel_tracks_jinja_query}'.format(**config),
                             '{project_id}:{target_dataset}.{bigquery_tracks}'.format(**config)]
            }
            aggregate_tracks = FlexibleOperator(aggregate_tracks_params).build_operator(flexible_operator_var)

            publish_postgres_tracks_params = {
                'task_id':'publish_postgres_tracks_{}'.format(name),
                'depends_on_past':True,
                'pool':'k8operators_limit' if flexible_operator_var == 'kubernetes' else 'bigquery',
                'docker_run':'{docker_run}'.format(**config),
                'image':'{docker_image}'.format(**config),
                'name':'pipe-vessels-publish-postgres-tracks-{}'.format(name),
                'dag':dag,
                'arguments':['publish_postgres_tracks',
                             '{date_range}'.format(**config),
                             '{project_id}:{target_dataset}.{bigquery_tracks}'.format(**config),
                             '{project_id}:{temp_dataset}'.format(**config),
                             '{temp_bucket}'.format(**config),
                             '{postgres_instance}'.format(**config),
                             '{postgres_connection_string}'.format(**config),
                             '{postgres_table_tracks}'.format(**config)]
            }
            publish_postgres_tracks = FlexibleOperator(publish_postgres_tracks_params).build_operator(flexible_operator_var)


            check_source_existance = config.get('check_source_existance', None)
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
