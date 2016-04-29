"""
Project: flask-rest
Author: Saj Arora
Description: General utility functions
"""
import hashlib
import re
from uuid import uuid4

from google.appengine.ext import ndb

from api.v1 import errors

EMAIL_REGEX = {
    'regex': r'^[-!#$%&\'*+\\.\/0-9=?A-Za-z^_`{|}~]+@([-0-9A-Za-z]+\.)+([0-9A-Za-z]){2,4}$',
    'name': 'email',
    'reverse': False
}

ALPHANUM_REGEX = {
    'regex': r'[^a-zA-Z0-9]',
    'name': 'alpha-numeric',
    'reverse': True
}

ALPHA_REGEX = {
    'regex': r'[^a-zA-Z]$',
    'name': 'alpha',
    'reverse': True
}

NUM_REGEX = {
    'regex': r'[^0-9]$',
    'name': 'numeric',
    'reverse': True
}



def constrain_string(string, minlen, maxlen):
    """Validation function constrains minimal and maximal lengths of string.

    Args:
        string (string): String to be checked
        minlen (int): Minimal length
        maxlen (int): Maximal length

    Returns:
        string: Returns given string

    Raises:
        InvalidUsage 400 with payload of min/maxlength
    """

    if len(string) < minlen:
        errors.create(400, {'minlength': minlen}, message='%s is too short' % string)
    elif len(string) > maxlen:
        errors.create(400, {'maxlength': maxlen}, message='%s is too long' % string)
    return string


def constrain_regex(string, regex):
    """Validation function checks validity of string for given regex.

    Args:
        string (string): String to be checked
        regex (object): Regular expression

    Returns:
        string: Returns given string

    Raises:
        InvalidUsage: If string doesn't match regex

    """
    regex_string = re.compile(regex.get('regex'))
    error = False
    if regex.get('reverse') and regex_string.search(string):
        error = True
    elif not regex.get('reverse') and not regex_string.search(string):
        error = True

    if error:
        errors.create(400, {'regex': regex.get('name')}, message='%s is not a %s' % (
            string, regex.get('name')
        ))
    return string

def create_validator(lengths=None, regex='', required=True, return_type=None):
    """This is factory function, which creates validator functions, which
    will then validate passed strings according to lengths or regex set at creation time

    Args:
        lengths (list): list of exact length 2. e.g [3, 7]
            indicates that string should be between 3 and 7 charactes
        regex (string): Regular expression
        required (bool): Wheter empty value '' should be accepted as valid,
            ignoring other constrains

    Returns:
        function: Function, which will be used for validating input
    """

    def validator_function(value, prop = None):
        """Function validates input against constraints given from closure function
        These functions are primarily used as ndb.Property validators

        Args:
            value (string): input value to be validated
            prop (string): ndb.Property name, which is validated

        Returns:
            string: Returns original string, if valid

        Raises:
            ValueError: If input isn't valid

        """
        # when we compare ndb.Property with equal operator e.g User.name == 'abc' it
        # passes arguments to validator in different order than as when e.g putting data,
        # hence the following parameters switch
        success = True
        result = None
        if isinstance(value, ndb.Property):
            value = prop
        if not required and value == '':
            return return_type('')
        elif required and not value:
            errors.create(400, {'required': value}, 'Missing required field')

        if regex:
            constrain_regex(value, regex)
        if lengths:
            constrain_string(value, lengths[0], lengths[1])
        return return_type(value)

    return validator_function


def password_hash(password, salt):
    """Hashes given plain text password with sha256 encryption
    Hashing is salted with salt configured by admin, stored in >>> model.Config

    Args:
        password (string): Plain text password

    Returns:
        string: hashed password, 64 characters

    """
    sha = hashlib.sha256()
    sha.update(password.encode('utf-8'))
    sha.update(salt)
    return sha.hexdigest()


def uuid():
    """Generates random UUID used as user token for verification, reseting password etc.

    Returns:
      string: 32 characters long string

    """
    return uuid4().hex