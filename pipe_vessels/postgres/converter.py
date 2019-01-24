import json
import csv
import re

geography_regex = re.compile(r"^.*\((.*)\)$")


def normalize_geography(value, geography_kind):
    match = geography_regex.match(value)
    points = match.group(1)
    return "{}({})".format(geography_kind, points)


def normalize_array(value):
    joined = ",".join([str(x) for x in value])
    result = "{{{}}}".format(joined)
    return result


def convert_json_to_csv(input_stream, output_file, record_to_row):
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
