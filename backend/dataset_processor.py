"""
Project: backend
Author: Saj Arora
Description: Helps with all the processing of datasets (worker functions)
"""
import StringIO
import logging

import re
from google.appengine.api import urlfetch
from google.appengine.ext import ndb

from api.v1 import SageModel, SageDateTime, SageInteger, SageString, SageBool, SageText, SageFloat, SageValidator


class Validators(object):
    @classmethod
    def convert_to_float(cls, value, prop=None):
        try:
            return float(re.sub("[^0-9|^.]", "", value))
        except:
             return 0.0

    @classmethod
    def convert_to_int(cls, value, prop=None):
        try:
            return int(re.sub("[^0-9]", "", value))
        except:
            return 0

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
            files=files,
            headers=[],
            errors=None,
            content=dict()
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
        dataset.status = {
            'code': 'headers_loaded'
        }
        dataset.parser_data = parser_data
        dataset.put()
        return 'ok'

    @classmethod
    def process_data(cls, **kwargs):
        key = kwargs.pop('key', None)
        # fetch the dataset
        dataset = ndb.Key(urlsafe=key).get()
        if not dataset:
            logging.error('Could not find dataset with key: %s' % key)
            return

        # generate a data model from the headers
        _headers = {}
        type_dict = {
            'string': [SageString, None],
            'integer': [SageInteger, 'convert_to_int'],
            'float': [SageFloat, 'convert_to_float'],
            'datetime': [SageDateTime, None],
            'bool': [SageBool, None],
            'text': [SageText, None]
        }
        for item in dataset.headers:
            data_type = type_dict.get(item.get('type'))
            _headers[item.get('name')] = data_type[0](validator_name=data_type[1])
        _validator = type('%sValidator' % str(dataset.name).capitalize(),
                                   (SageValidator,), {'convert_to_int': Validators.convert_to_int,
                                                      'convert_to_float': Validators.convert_to_float})
        _headers['validator'] = _validator
        _model = type('%sModel' % str(dataset.name).capitalize(), (SageModel,), _headers)
        files = dataset.parser_data.get('files', [])
        for file in files:
            result = urlfetch.Fetch(file, method='get', validate_certificate=True)
            if result.status_code == 200:
                import csv
                all_records = []
                f = StringIO.StringIO(result.content)
                reader = csv.reader(f, skipinitialspace=True)
                headers = []
                for i, row in enumerate(reader):
                    current_record = {}
                    if i == 0:
                        headers = [x.lower() for x in row]
                    else:
                        if len(row) != len(headers):
                            dataset.status = {'code': 'Failed', 'error': 'Invalid CSV. File: %s. Line: %d' % (file, i)}
                            return

                        for j, value in enumerate(row):
                            current_record[headers[j]] = value

                        for k, v in current_record.iteritems():
                            if getattr(_model, k).validator_name:
                                current_record[k] = _model.get_validator().create(getattr(_model, k).validator_name)(v)
                        all_records.append(_model(**current_record))
                ndb.put_multi(all_records)
        return 'ok'


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
