"""
Project: ProjectEos-Server
Author: Saj Arora
Description: Model for Dataset
"""

import json

from google.appengine.api.taskqueue import taskqueue

from api.v1 import SageString, SageText, SageInteger, SageResource, SageController, SageMethod, errors, helper, util, SageBool, SageJson


def add_dataset(self, resource, **kwargs):
    _Model = resource.get_model()
    args = helper.parse_args_for_model(_Model, [{'name': 'file', 'required': True, 'action': 'append'}])
    args['secret'] = util.uuid()
    args['headers'] = []
    files = args.pop('file')
    model = _Model(**args)
    model.status = dict(code='Started...')
    model.put()

    # start the processing
    response = model.to_dict()
    response['secret'] = model.secret # force show the secret on creation

    task = taskqueue.add( # first process headers
        queue_name='processor-queue',
        url='/tasks/process_headers',
        payload= json.dumps(dict(
            key=model.get_key_urlsafe(),
            files=files)
        ))

    return response


def unique_name(self, name):
    """Validates if given name is not in datastore"""
    name = name.lower()
    if self.model.get_by('name', name):
        errors.create(400, payload={'name': 'uniqueName'}, message="Sorry, a dataset with this name already exists.")
    return name


dataset_module = SageResource(
    'dataset_module',
    'datasets',
    model_dict={
        'name': SageString(required=True, validator_name='unique_name'),
        'email': SageString(required=True, validator_name='email'),
        'secret': SageString(editable=False, public=False),
        'description': SageText(required=True),
        'total_records': SageInteger(editable=False),
        'status': SageJson(editable=False),
        'headers': SageJson(repeated=True),
        'parser_data': SageJson(public=False, editable=False),
        'is_ready': SageBool(editable=False, default=False)
    },
    validator_dict={
        'unique_name': unique_name
    },
    endpoints={
        SageResource.ALL: [
            SageMethod.GET,
            SageMethod.POST
        ]
    },
    controllers={
        SageResource.ALL + SageMethod.POST: SageController(add_dataset, SageMethod.POST)
    },
    authenticate=False
)
