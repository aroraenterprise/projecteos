"""
Project: flask-rest
Author: Saj Arora
Description: A controller for a resource e.g GET controller for user resource
"""
import json
import re

from flask import request
from flask_restful import reqparse
from google.appengine.ext import ndb

from api.v1 import errors
import helper
from .sage_methods import SageMethod
from .response import make_empty_ok_response, make_list_response
from .validator import ArgumentValidator
import pydash as _


class SageController(object):
    ONE = 'one'
    ALL = 'all'

    def __init__(self, fxn, method=SageMethod.GET, key_name=None, authenticate=None):
        self.key_name = key_name
        self.authenticate = authenticate

        if method not in SageMethod.ALL:
            raise Exception("Invalid method for controller: %s" % method, __file__, __name__)
        self.method = method

        if not hasattr(fxn, '__call__'):
            raise Exception("fxn: %s for controller object must be a callable" % repr(fxn),
                            __file__, __name__)

        self._fxn = fxn

    def get_fxn(self, resource):
        """
        Wraps the fxn to pull out a key if there is one
        :param resource: Resource class that will be calling this controller -> link to model
        :return:
        """
        _key_name = self.key_name or ''
        fxn = self._fxn
        authenticate = self.authenticate or resource.requires_authentication()

        def wrapped_fxn(self, **kwargs):
            account = None
            if authenticate and resource.get_auth():
                account = resource.get_auth().authenticate()

            key_name = '%skey' % _key_name
            key = None
            if key_name in kwargs:
                key = kwargs.pop(key_name)
            return fxn(self, key=key, account=account, resource=resource, **kwargs)

        return wrapped_fxn


COMP_EQUALITY = '='
COMP_LESS_THAN = '<'
COMP_GREATER_THAN = '>'
_DEFAULT_LIMIT = 20


def sage_list_controller_fxn(self, resource, **kwargs):
    _Model = resource.get_model()

    parser = reqparse.RequestParser()
    parser.add_argument('limit', type=int)
    parser.add_argument('cursor', type=ArgumentValidator.create('cursor'))
    parser.add_argument('order')
    parser.add_argument('filter', action='append')
    args = parser.parse_args()

    filter_node = None
    if args.get('filter'):
        filters = []
        for filter in args.get('filter'):
            comparison = None
            result = []
            for delimiter in [COMP_EQUALITY, COMP_GREATER_THAN, COMP_LESS_THAN]:
                result = [s.strip() for s in re.split(delimiter, filter)]
                if len(result) == 2:
                    comparison = delimiter
                    break
            if comparison and result[0] in _Model._properties:
                result[1] = _Model._properties.get(result[0]).validator_type(result[1])

                filters.append(
                    ndb.FilterNode(result[0], comparison, result[1])
                )
                if comparison != COMP_EQUALITY:  # sort order must be altered
                    args['order'] = getattr(_Model, result[0])

        if len(filters) > 0:
            filter_node = ndb.AND(*filters)

    items_future = _Model.query(filters=filter_node).order(args.order or -_Model.modified) \
        .fetch_page_async(args.limit or _DEFAULT_LIMIT, start_cursor=args.cursor)

    total_count_future = _Model.query(filters=filter_node).count_async(keys_only=True)
    items, next_cursor, more = items_future.get_result()
    items = [i.to_dict() for i in items]
    return make_list_response(items, next_cursor, more, total_count_future.get_result())


def sage_create_controller_fxn(self, resource, **kwargs):
    _Model = resource.get_model()

    if 'list' in request.json and isinstance(request.json.get('list'), list): # it is a list of models
        props = _Model.get_editable_properties()  # list of props
        validators = dict()
        if _Model.get_validator():
            for prop in props:
                validators[prop._name] = _Model.get_validator().create(prop.validator_name,
                                                                       return_type=prop.validator_type)

        entities = []
        for item in request.json.get('list'):
            entity_dict = dict()
            for k, v in item.iteritems():
                v = v.encode('utf-8')
                prop = getattr(_Model, k)
                if prop._name in validators:
                    v = validators.get(prop._name)(v)
                entity_dict[k] = v
            entities.append(_Model(**entity_dict))
        ndb.put_multi(entities)
        entities = [x.to_dict() for x in entities]
        return make_list_response(entities, None, False, len(entities))
    else:
        args = helper.parse_args_for_model(_Model)
        model = _Model(**args)
        model.put()
        return model.to_dict()


def sage_get_controller_fxn(self, key, resource, **kwargs):
    model = None
    try:
        model = ndb.Key(urlsafe=key).get()
    except:
        errors.create(400)
    if not model:
        errors.create(404)
    return model.to_dict()


def sage_update_controller_fxn(self, key, resource, **kwargs):
    model = helper.get_model_by_key_or_error(key)
    ## update the model
    args = helper.parse_args_for_model(model)
    model.populate(**args)
    model.put()
    return model.to_dict()


def sage_remove_controller_fxn(self, key, resource, **kwargs):
    try:
        ndb.Key(urlsafe=key).delete()
        return make_empty_ok_response()
    except:
        errors.create(400, message="Invalid request to remove entity.")


def get_default_controllers(name):
    return {
        SageController.ALL + SageMethod.GET: SageController(sage_list_controller_fxn, SageMethod.GET, key_name=name),
        SageController.ALL + SageMethod.POST: SageController(sage_create_controller_fxn, SageMethod.POST, key_name=name),
        SageController.ONE + SageMethod.GET: SageController(sage_get_controller_fxn, SageMethod.GET, key_name=name),
        SageController.ONE + SageMethod.PUT: SageController(sage_update_controller_fxn, SageMethod.PUT, key_name=name),
        SageController.ONE + SageMethod.DELETE: SageController(sage_remove_controller_fxn, SageMethod.DELETE, key_name=name)
    }
