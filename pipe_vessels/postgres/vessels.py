import sys
from pipe_vessels.postgres.converter import convert_json_to_csv


def record_to_row(record):
    return [
        record["seg_id"],
        record["vessel_id"]
    ]


convert_json_to_csv(sys.stdin, sys.argv[1], record_to_row)
