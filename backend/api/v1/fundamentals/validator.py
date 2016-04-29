"""
Project: flask-rest
Author: Saj Arora
Description: Base Validator for Parsing/Validating input
"""
import re

import datetime
import six
from flask_restful import reqparse
from google.appengine.ext.ndb import Cursor
from pydash import _

import util
from api.v1 import errors


class NamingConvention(object):
    CAPS = "caps"
    CAMEL_CASE = "camel_case"
    SNAKE_CASE = "snake_case"

    @classmethod
    def _process(cls, name, model_case, request_case):
        if not name:
            raise Exception("Improper name for processing: %s" % name, __file__, __name__)

        # no change needed
        if model_case == request_case:
            return name, None

        if model_case == cls.SNAKE_CASE:  # changing this involves getting rid of underscores
            new_name = ''.join([x.capitalize() for x in name.split('_')])
            if request_case == cls.CAMEL_CASE:  # make first letter small
                return new_name[:1].lower() + new_name[1:], name
            return new_name, name

        if request_case == cls.SNAKE_CASE:  # have to add underscores:
            return '_'.join(re.findall('[A-Z][^A-Z]*', name[:1].upper() + name[1:])).lower(), name

        if request_case == cls.CAPS:  # change the first letter to capital
            return name[:1].upper() + name[1:], name
        else:  # lower the first letter
            return name[:1].lower() + name[1:], name

    @classmethod
    def process(cls, name, model_case=SNAKE_CASE, request_case=SNAKE_CASE):
        return cls._process(name, model_case, request_case)

    @classmethod
    def convert(cls, name, to_case=SNAKE_CASE, from_case=SNAKE_CASE):
        value, _ = cls._process(name, from_case, to_case)
        return value


text_type = lambda x: six.text_type(x)


class SageArgument(reqparse.Argument):
    def __init__(self, name, default=None, dest=None, required=False, ignore=False, type=text_type,
                 location=('json', 'values',), choices=(), action='store', help=None, operators=('=',),
                 case_sensitive=True, store_missing=True, model_case=NamingConvention.SNAKE_CASE,
                 request_case=NamingConvention.SNAKE_CASE):
        self.request_case = request_case
        self.model_case = model_case

        # if request_case != model_case then process them to be the same and make dest the model_case
        # else leave name alone and don't change dest
        name, new_dest = NamingConvention.process(name, model_case, request_case)

        # only change destination to the new_dest if there wasn't a destination already set
        dest = dest or new_dest

        super(SageArgument, self).__init__(name, default, dest, required, ignore, type, location, choices, action, help,
                                           operators, case_sensitive, store_missing)


class SageValidator(object):
    """Base factory class for creating validators for ndb.Model properties
    To be able to create validator for some property, extending class has to
    define attribute which has to be one of these:
        list - with 2 elements, determining min and max length of string
        regex - which will be validated against string
        function - validation function

    After defining attributes we will be able to create respective validator functions.

    Examples:
        Let's say we want to create validator factory for our new model
        class MySuperValidator(BaseValidator):
            short_name = [2, 4]

        Now if we call MySuperValidator.create('short_name') it returns
         function, which will throw error of string is not between 2-4 chars
         The same goes with if short_name was regex, and if it was function,
         the function itself is returned as validator

     Creating validation functions this way is useful for passing it as
     'validator' argument to ndb.Property constructor and also passing it as 'type'
     argument to reqparse.RequestParser, when adding argument via add_argument
    """

    DATE_TIME = 'date_time'

    @classmethod
    def create(cls, name, return_type=None):
        """Creates validation function from given attribute name

        Args:
            name (string): Name of attribute
            required (bool, optional) If false, empty string will be always accepted as valid

        Returns:
            function: validation function
            :param return_type:
        """
        return_type = return_type or str
        if not name:  # no name given -> just return a do nothing function
            def empty_validator_function(value=None, prop=None):
                return return_type(value)

            return empty_validator_function

        ### Date Time validator that converts string datetimes/timestamps to proper datetime objects ###
        if name == SageValidator.DATE_TIME:
            # parse date time
            def date_time_parser(value=None, prop=None):
                temp_datetime = None
                try:  # timestamp approach first
                    temp_datetime = datetime.datetime.fromtimestamp(int(value))
                except ValueError:
                    temp_datetime = None
                if temp_datetime:
                    return temp_datetime

                try:  # iso format next
                    temp_datetime = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
                except ValueError:
                    temp_datetime = None

                if temp_datetime:
                    return temp_datetime
                errors.create(400, message='Invalid date time format')

            return date_time_parser

        attr = getattr(cls, name)
        if _.is_list(attr):
            return util.create_validator(lengths=attr, return_type=return_type)
        elif _.is_function(attr):
            return attr
        elif 'regex' in attr and 'lengths' in attr:  # contains both regex and lengths
            return util.create_validator(regex=attr.get('regex'), lengths=attr.get('lengths'),
                                         return_type=return_type)
        else:  # just a regex
            return util.create_validator(regex=attr, return_type=return_type)


class ArgumentValidator(SageValidator):
    """This validator class contains attributes and methods for validating user's input,
    which is not associated with any particular datastore model, but still needs
    to be validated

    Attributes:
      feedback (list): determining min and max lengths of feedback message sent to admin

    """

    @classmethod
    def cursor(cls, cursor):
        """Verifies if given string is valid ndb query cursor
        if so returns instance of it

        Args:
            cursor (string): Url encoded ndb query cursor

        Returns:
            google.appengine.datastore.datastore_query.Cursor: ndb query cursor

        Raises:
           ValueError: If captcha is incorrect
        """
        if not cursor:
            return None
        return Cursor(urlsafe=cursor)
