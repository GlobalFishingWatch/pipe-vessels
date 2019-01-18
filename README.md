# Vessels pipeline

This repository contains the vessels pipeline, a pipeline which extracts and compiles detailed vessel information.

# Running

## Dependencies

You just need [docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/) in your machine to run the pipeline. No other dependency is required.

## Setup

The pipeline reads it's input from BigQuery, so you need to first authenticate with your google cloud account inside the docker images. To do that, you need to run this command and follow the instructions:

```
docker-compose run gcloud auth login
```

## Configuration

The pipeline exposes the following standard settings:

* `pipe_vessels.docker_run`: Command to run docker inside the airflow server.
* `pipe_vessels.project_id`: Google cloud project id containing all the resources that running this pipeline requires.
* `pipe_vessels.temp_bucket`: GCS bucket where temp files may be stored to.
* `pipe_vessels.pipeline_bucket`: GCS bucket where all final files generated by this pipeline may be stored to.
* `pipe_vessels.pipeline_dataset`: BigQuery dataset containing various tables used in this pipeline.

In addition to this, the following custom settings are required for this
pipeline, and come with default values:

* `pipe_vessels.scored_messages`: BigQuery table to read scored messages from, used as the source for track aggregation. Defaults to `messages_scored_`

Finally, the following custom entries do not provide a default value and must be manually configured before using this pipeline:

* `pipe_vessels.postgres_instance`: CloudSQL postgres instance where the tracks are published to.
* `pipe_vessels.postgres_connection_string`: Connection string for the postgres database to publish the tracks to.
* `pipe_vessels.fishing.postgres_table`: Table in postgres to publish the tracks to.

# License

Copyright 2017 Global Fishing Watch

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
