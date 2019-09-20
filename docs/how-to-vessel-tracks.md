## Query signature

All tracks query need to contain the following attributes:
```
    STRING seg_id
    STRING vessel_id
    TIMESTAMP timestamp
    ST_GEOGPOINT position
    FLOAT speed  (OPTIONAL)
    FLOAT course (OPTIONAL)
    FLOAT score  (OPTIONAL)
```

## Example vessel track format

Imagine that we cant to eecute the following query 

```
#standardSQL
WITH
  ########################################################
  # Extract the messages we are going to process
  ########################################################
  messages AS (
  SELECT
    sv.seg_id,
    sv.vessel_id,
    m.timestamp,
    ST_GEOGPOINT(m.lon, m.lat) AS position,
    IFNULL(m.nnet_score, m.logistic_score) AS score,
    m.speed,
    m.course
  FROM
    `MESSAGES_SCORED_TABLE*` AS m
  INNER JOIN
    `SEGMENT_INFO_TABLE` AS si
  USING
    (seg_id)
  INNER JOIN
    `VESSEL_INFO_TABLE` AS sv
  USING
    (seg_id)
  WHERE
    _TABLE_SUFFIX BETWEEN '{{ start_yyyymmdd }}'
    AND '{{ end_yyyymmdd }}'
    AND si.noise = false
    AND si.pos_count > 5
    AND m.lat IS NOT NULL
    AND m.lon IS NOT NULL
    AND sv.vessel_id_rank = 1)
SELECT
  seg_id,
  vessel_id,
  timestamp,
  position,
  score,
  speed,
  course
FROM
  messages
```

Received parameters are `start_yyyymmdd`, `end_yyyymmdd`, `start_yyyymmdd_nodash`, `end_yyyymmdd_nodash`. These
parameters will change depending if the pipe is run in daily, monthly or yearly mode.


## Airflow configuration

Since we need to pass this query to AIRFLOW, we need to make sure it is writtent in a JSON  format way, for example the following
is the configuration used for the sharks layer:

```
  "configurations": [
    {
      "bigquery_tracks": "tracks", 
      "bigquery_vessel_info_query": "SELECT shark_id vesselId, species_name, scientific_name, total_length_cm, tagging_date, shark_name, sex, observations, FORMAT_TIMESTAMP(\"%Y-%m-%d\", min(timestamp)) AS `start`, FORMAT_TIMESTAMP(\"%Y-%m-%d\", max(timestamp)) AS `end` FROM `world-fishing-827.shark_prototype.GHRI_caribbean_mako_live` GROUP BY 1,2,3,4,5,6,7,8", 
      "bigquery_vessel_tracks_jinja_query": "WITH messages AS ( SELECT CAST(m.shark_id AS STRING) as seg_id, CAST(m.shark_id AS STRING) as vessel_id, m.timestamp, ST_GEOGPOINT(m.lon, m.lat) AS position FROM `world-fishing-827.shark_prototype.GHRI_caribbean_mako_live` m WHERE m.lat IS NOT NULL AND m.lon IS NOT NULL AND timestamp >= TIMESTAMP(\"{{ '{{start_yyyymmdd}}' }}\") AND timestamp < TIMESTAMP(\"{{ '{{end_yyyymmdd}}' }}\")) SELECT seg_id, vessel_id, timestamp, position, 0.0 as score, 0.0 as speed, 0.0 as course  FROM messages", 
      "elasticsearch_index_alias": "vessels-sharks-v20190816", 
      "elasticsearch_index_mappings": "{ \"mappings\": { \"vessels\": { \"properties\": { \"vesselId\": { \"type\": \"keyword\" }, \"start\": { \"type\": \"date\" }, \"end\": { \"type\": \"date\" }, \"shark_name\": { \"type\": \"text\" }, \"scientific_name\": { \"type\": \"text\" }, \"total_length_cm\": { \"type\": \"text\" }, \"tagging_date\": { \"type\": \"date\" }, \"sex\": { \"type\": \"text\" }, \"observations\": { \"type\": \"text\" } } } } }", 
      "name": "sharks", 
      "postgres_table_tracks": "sharks_v20190816_tracks", 
      "target_dataset": "scratch_enrique_ttl_60_days"
    }
  ],
```

Check how the date is passed in the `bigquery_vessel_tracks_jinja_query`: ` timestamp >= TIMESTAMP(\"{{ '{{start_yyyymmdd}}' }}\") AND timestamp < TIMESTAMP(\"{{ '{{end_yyyymmdd}}' }}\")) `