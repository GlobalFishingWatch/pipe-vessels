import json
import sys
import datetime as dt
import itertools as it
import json
import re
from pipe_vessels.elasticsearch.server import ElasticSearchServer


def batch(iterable, size):
    args = [iter(iterable)] * size
    return it.izip_longest(*args)


bq_datetime_regex = re.compile('^(\d\d\d\d-\d\d-\d\d) (\d\d:\d\d:\d\d) UTC$')


def to_elasticsearch_datetime(value):
    match = bq_datetime_regex.match(value)
    return "{}T{}Z".format(match.group(1), match.group(2))


def line_to_elasticsearch_bulk_command(line):
    record = json.loads(line)
    command = {"index": {"_index": unique_index_name,
                         "_type": "vessel", "_id": record["vessel_id"]}}
    data = {
        "vessel_id": record["vessel_id"],
        "start": to_elasticsearch_datetime(record["first_timestamp"]),
        "end": to_elasticsearch_datetime(record["last_timestamp"]),
        "shipname": record.get("shipname", {}).get("value"),
        "callsign": record.get("callsign", {}).get("value"),
        "imo": record.get("imo", {}).get("value"),
    }
    return [command, data]



# Configuration options
server_url = sys.argv[1]
server_auth = sys.argv[2]
index_name = sys.argv[3]
index_schema = sys.argv[4]

# Derived configuration options
timestamp = dt.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
unique_index_name = '{}-{}'.format(index_name, timestamp)

# Open a base http connection to elasticsearch server
server = ElasticSearchServer(server_url, server_auth)

# Get where the current alias is pointing to later remove old indices
print "Obtaining alias information for the current index"
alias_info = server.alias_information(index_name)
old_indices = list(alias_info.keys())
print "The alias is currently pointing to {}".format(old_indices)

# Precreate the index so that we can setup proper mappings
with open(index_schema, 'rb') as schema_file:
    print "Reading schema from {}".format(index_schema)
    schema = schema_file.read()
    print "Creating index {}".format(unique_index_name)
    server.create_index(unique_index_name, schema)

try:
    # Process the records in batches
    bulk_commands = it.imap(
        line_to_elasticsearch_bulk_command, iter(sys.stdin))
    batched_commands = batch(bulk_commands, 5000)

    # For each batch, push it as a bulk payload
    for batch in batched_commands:
        print "Indexing batch"
        server.bulk(it.ifilter(lambda x: x is not None, batch))

    # Update the alias to point to the new index
    print "Updating index alias which was pointing to {} to point to the new index {}".format(
        old_indices, unique_index_name)
    server.alias({
        "actions": [
            {"add": {"index": unique_index_name, "alias": index_name}},
        ]
    })
except Exception as e:
    print "Exception while importing records to elastic search. {}".format(e)
    print "Removing new index {}  as the import process failed".format(
        unique_index_name)
    server.drop_index(unique_index_name)

# Remove the old indices
for old_index in old_indices:
    server.drop_index(old_index)