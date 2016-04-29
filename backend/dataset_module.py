"""
Project: ProjectEos-Server
Author: Saj Arora
Description: Model for Dataset
"""
from api.v1 import SageString, SageModel, SageText, SageInteger, SageResource, SageController, get_default_controllers


class DatasetModel(SageModel):
    name = SageString(required=True)
    email = SageString(required=True)
    secret = SageString(required=True)
    description = SageText(required=True)
    total_records = SageInteger()

default_controllers = get_default_controllers('datasets')
print default_controllers
# dataset_module = SageResource(
#     'dataset_module',
#     'datasets',
#     controllers={
#         '': [SageController(parse_fxn, SageMethod.POST),
#
#     },
#     authenticate=False
# )