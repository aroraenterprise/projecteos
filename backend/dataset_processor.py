"""
Project: backend
Author: Saj Arora
Description: Helps with all the processing of datasets (worker functions)
"""
import StringIO
import logging

from google.appengine.api import urlfetch
from google.appengine.ext import ndb


class DatasetProcessor(object):
    @classmethod
    def process_headers(cls, **kwargs):
        key = kwargs.pop('key', None)
        # fetch the dataset
        dataset = ndb.Key(urlsafe=key).get()
        if not dataset:
            logging.error('Could not find dataset with key: %s' % key)
            return

        files = kwargs.pop('files', [])
        parser_data = dict(
            files = files,
            headers = [],
            errors = None,
            content = dict()
        )
        for file in files:
            result = urlfetch.Fetch(file, method='get', validate_certificate=True)
            if result.status_code == 200:
                import csv
                f = StringIO.StringIO(result.content)
                reader = csv.reader(f, skipinitialspace=True)
                records = []
                for i, row in enumerate(reader):
                    if i == 0:
                        parser_data['headers'] = [x.lower() for x in row]
                    else:
                        if len(row) != len(parser_data['headers']):
                            parser_data['errors'] = 'Invalid CSV. File: %s. Line: %d' % file, i
                            return

                        for j, value in enumerate(row):
                            parser_data['content'][parser_data['headers'][j]] = value

        dataset.headers = [{'name': x, 'type': 'string'} for x in parser_data['headers']]
        dataset.parser_data = parser_data
        dataset.put()

    @classmethod
    def process_data(cls, **kwargs):
        print kwargs


fxns = [
    {
        'name': 'process_headers',
        'value': DatasetProcessor.process_headers
    },
    {
        'name': 'process_data',
        'value': DatasetProcessor.process_data
    },
]
