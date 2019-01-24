import sys
from pipe_vessels.postgres.converter import convert_json_to_csv, normalize_geography, normalize_array


def record_to_row(record):
    return [
        record["seg_id"],
        normalize_geography(record["seg_geography"], "MULTIPOINT"),
        normalize_array(record["times"]),
        normalize_array(record["scores"]),
        normalize_array(record["speeds"]),
        normalize_array(record["courses"])
    ]


convert_json_to_csv(sys.stdin, sys.argv[1], record_to_row)
