"""
Project: flask-rest
Author: Saj Arora
Description: Handle Email/Password authentication
"""
import base64

import jwt
from google.appengine.ext import ndb

import config
from api.v1.fundamentals import util
from api.v1.auth_module import AuthModel
from api.v1.auth_module.authority import AuthType

class EmailAuth(object):

    auth_type = AuthType.EMAIL
    _minLen = 6
    _maxLen = 100
    _uid = ''

    def __init__(self, email, password):
        self._uid = self.email = email
        self.password = util.password_hash(password, config.PASSWORD_SALT)

    def is_valid(self):
        if self.email and util.constrain_regex(self.email, util.EMAIL_REGEX) \
                and self.password and util.constrain_string(self.password, self._minLen, self._maxLen):
            return True
        return False

    def get_id(self):
        return base64.b64encode(str(self.auth_type) + '_' + self._uid)

    def get_key(self):
        return ndb.Key(AuthModel, self.get_id())

    def is_unique(self):
        auth_key = self.get_key()
        if not auth_key.get():
            return True
        return False

    def get_jwt(self):
        return jwt.encode(dict(email=self.email, password=self.password),
                          config.JWT_SECRET)
