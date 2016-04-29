"""
Project: flask-rest
Author: Saj Arora
Description: 
"""
from flask_restful import reqparse
from google.appengine.ext import ndb

from api.v1 import errors


def parse_args_for_model(model):
    parser = reqparse.RequestParser()

    # get all editable properties
    for prop in model.get_editable_properties():
        parser_type = prop.validator_type
        if model.get_validator():
            parser_type = model.get_validator().create(prop.validator_name, return_type=prop.validator_type)
        parser.add_argument(prop._name, type=parser_type, required=prop.required)

    return parser.parse_args()


def get_model_by_key_or_error(key):
    model = None
    try:
        model = ndb.Key(urlsafe=key).get()
    except:
        errors.create(400, message="Invalid model key: %s" % key)
    if not model:
        errors.create(404)
    return model
