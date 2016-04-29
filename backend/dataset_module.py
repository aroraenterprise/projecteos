"""
Project: ProjectEos-Server
Author: Saj Arora
Description: Model for Dataset
"""
from api.v1 import SageString, SageModel, SageText, SageInteger, SageResource, SageController, get_default_controllers, \
    SageMethod, errors, helper, util


def add_dataset(self, resource, **kwargs):
    args = helper.parse_args_for_model(resource.get_model())
    args['secret'] = util.uuid()
    return dict(**args)


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
        'secret': SageString(),
        'description': SageText(required=True),
        'total_records': SageInteger()
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
