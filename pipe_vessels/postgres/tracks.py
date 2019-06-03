"""Short script to convert track records exported from BigQuery to the CSV format Postgres needs."""

import sys
import json
import csv

def record_to_row(record):
    return [
        record["seg_id"],
        record["vessel_id"],
        record["timestamp"],
        record["position"],
        record.get("score", ""),
        record.get("speed", ""),
        record.get("course", ""),
    ]


input_stream = sys.stdin
output_file = sys.argv[1]
with open(output_file, "wb+") as f:
    writer = csv.writer(f)

    for line in input_stream:
        record = json.loads(line)

        try:
            row = record_to_row(record)
            writer.writerow(row)
        except:
            print("Unable to convert record to csv row at {}".format(record))
            raise
