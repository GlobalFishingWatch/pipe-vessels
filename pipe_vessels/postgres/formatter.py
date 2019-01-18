import sys
import json
import csv
import re

geography_regex = re.compile(r"^.*\((.*)\)$")

csv_file = sys.argv[1]

def normalize_array_field(record, field):
    print("")
    joined = ",".join([str(x) for x in record[field]])
    result = "{{{}}}".format(joined)
    return result

with open(csv_file, "wb+") as f:
    writer = csv.writer(f)

    for line in sys.stdin:
        record = json.loads(line)

        # Normalize points and multipoints into multipoints
        match = geography_regex.match(record['seg_geography'])
        points = match.group(1)
        normalized_geography = "MULTIPOINT({})".format(points)

        try:
            writer.writerow([
                record["seg_id"],
                normalized_geography,
                normalize_array_field(record, "times"),
                normalize_array_field(record, "scores"),
                normalize_array_field(record, "speeds"),
                normalize_array_field(record, "courses")
            ])
        except:
            print("Unable to convert record to csv at {}".format(record))
            raise
