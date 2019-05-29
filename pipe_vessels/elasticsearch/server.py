"""Utility classes for accessing elastc search through it's HTTP API"""

import httplib
import base64
import json


class ElasticSearchServer:
    def __init__(self, server_url, server_auth):
        self.connection = httplib.HTTPSConnection(server_url)
        self.auth_header = {
            'authorization': 'Basic {}'.format(base64.b64encode(server_auth))
        }

    def create_index(self, name, schema):
        url = '/{}'.format(name)
        self.connection.request('PUT', url, schema, self.auth_header)
        response = self.connection.getresponse()
        body = response.read()
        if response.status != 200:
            raise RuntimeError(
                'Unable to create index {}'.format(body))

    def drop_index(self, name):
        url = '/{}'.format(name)
        self.connection.request('DELETE', url, None, self.auth_header)
        response = self.connection.getresponse()
        body = response.read()
        if response.status != 200:
            raise RuntimeError(
                'Unable to drop index {}'.format(body))

    def bulk(self, commands):
        lines = [json.dumps(entry)
                 for command in commands for entry in command]
        chunk = "\n".join(lines)
        octects = chunk.encode('utf-8')
        url = '/_bulk'
        self.connection.request("POST", url, octects, self.auth_header)
        response = self.connection.getresponse()
        body = response.read()
        if response.status != 200:
            raise RuntimeError(
                'Elastic Search bulk API returned wrong status code {}'.format(response.status))

        result = json.loads(body)
        if result['errors']:
            raise RuntimeError(
                'Elastic Search bulk API could not index records {}'.format(result))

    def alias(self, actions):
        url = '/_aliases'
        payload = json.dumps(actions)

        self.connection.request('POST', url, payload, self.auth_header)
        response = self.connection.getresponse()
        body = response.read()
        if response.status != 200:
            raise RuntimeError(
                'Unable to perform alias operation {}'.format(body))

    def alias_information(self, name):
        url = '/_alias/{}'.format(name)
        self.connection.request('GET', url, None, self.auth_header)
        response = self.connection.getresponse()
        body = json.loads(response.read())
        if response.status != 200:
            return {}
        else:
            return body
