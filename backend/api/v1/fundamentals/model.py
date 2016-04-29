"""
Project: flask-rest
Author: Saj Arora
Description: Base model for all v1 models to inherit. Provides basic functions and
adds properties such as created, modified and version automatically
"""
from datetime import date
import pydash as _

from .validator import SageValidator
from google.appengine.ext import ndb


class SageProperty(ndb.Property):
    public = True
    editable = True
    validator_name = None
    validator_type = None

    def __init__(self, public=True, editable=True, validator_name=None,
                 validator_type=str, **kwds):
        super(SageProperty, self).__init__(**kwds)
        self.public = public
        self.editable = editable
        self.validator_name = validator_name
        self.validator_type = validator_type
        self.required = kwds.get('required', False)


class SageString(SageProperty, ndb.StringProperty):
    pass


class SageText(SageProperty, ndb.TextProperty):
    pass


class SageFloat(SageProperty, ndb.FloatProperty):
    def __init__(self, validator_type=float, **kwds):
        super(SageFloat, self).__init__(validator_type=validator_type, **kwds)


class SageInteger(SageProperty, ndb.IntegerProperty):
    def __init__(self, validator_type=int, **kwds):
        super(SageInteger, self).__init__(validator_type=validator_type, **kwds)


class SageKey(SageProperty, ndb.KeyProperty):
    pass


class SageGravatar(SageProperty, ndb.StringProperty):
    pass


class SageJson(SageProperty, ndb.JsonProperty):
    def __init__(self, **kwds):
        super(SageJson, self).__init__(validator_type=dict, **kwds)


class SageStructured(SageProperty, ndb.StructuredProperty):
    pass


class SageBool(SageProperty, ndb.BooleanProperty):
    pass


class SageDateTime(ndb.DateTimeProperty):
    public = True
    editable = True
    validator_name = SageValidator.DATE_TIME
    validator_type = str

    def __init__(self, public=True, editable=True, **kwds):
        super(SageDateTime, self).__init__(**kwds)
        self.public = public
        self.editable = editable
        self.required = kwds.get('required', False)


class SageComputed(ndb.ComputedProperty):
    public = True
    editable = False
    validator_name = None
    validator_type = str

    def __init__(self, fxn, public=True, editable=False, validator_type=validator_type, **kwds):
        super(SageComputed, self).__init__(fxn, **kwds)
        self.public = public
        self.editable = editable
        self.validator_type = validator_type
        self.required = kwds.get('required', False)


class SageModel(ndb.Model):
    created = SageDateTime(auto_now_add=True, editable=False)
    modified = SageDateTime(auto_now=True, editable=False)
    validator = None

    def get_id(self):
        return self.key.id()

    def get_key_urlsafe(self):
        return self.key.urlsafe()

    @classmethod
    def get_by(cls, name, value, keys_only=None):
        """Gets model instance by given property name and value
        :param name:
        :param value:
        :param keys_only:
        """
        return cls.query(getattr(cls, name) == value).get(keys_only=keys_only)

    def to_dict(self, include=None):
        """Return a dict containing the entity's property values, so it can be passed to client

        Args:
            include (list, optional): Set of property names to include, default all properties
        """
        _MODEL = type(self)
        repr_dict = {}
        if include is None:
            include = []
            for name, prop in _MODEL._properties.iteritems():
                if hasattr(prop, 'public') and getattr(prop, 'public', False):
                    include.append(name)

        for name in include:
            # check if this property is even allowed to be public
            # or has a value set
            if not hasattr(self, name):
                continue

            value = getattr(self, name)
            if type(getattr(_MODEL, name)) == ndb.StructuredProperty:
                if isinstance(value, list):
                    items = []
                    for item in value:
                        items.append(item.to_dict(include=None))
                    repr_dict[name] = items
                else:
                    repr_dict[name] = value.to_dict(include=None)
            elif isinstance(value, date):
                repr_dict[name] = value.isoformat()
            elif isinstance(value, ndb.Key):
                repr_dict[name] = value.urlsafe()
            else:
                repr_dict[name] = value

            if self._key:
                repr_dict['key'] = self.get_key_urlsafe()
        return repr_dict

    @classmethod
    def get_editable_properties(cls):
        result = []
        for name, value in cls._properties.iteritems():
            if (isinstance(value, SageProperty) or isinstance(value, SageDateTime)) and value.editable:
                result.append(value)

        return result

    @classmethod
    def get_validator(cls):
        """
        Returns the validator class for this resource
        but if no validator then returns the SageValidator class
        :return:
        """
        cls.validator.model = cls
        return cls.validator or SageValidator

    def _validate(self):
        """
        Validate all properties and your own model.
        """
        for name, prop in self._properties.iteritems():
            value = getattr(self, name, None)
            prop._do_validate(value)
