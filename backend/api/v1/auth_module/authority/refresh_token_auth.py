"""
Project: flask-rest
Author: Saj Arora
Description: Handle Email/Password authentication
"""

import jwt
from google.appengine.ext import ndb
from jwt import DecodeError

import config
from api.v1.auth_module.authority import AuthType


class RefreshTokenAuth(object):

    auth_type = AuthType.REFRESH_TOKEN
    _uid = ''
    _valid_token = True

    def __init__(self, token):
        self._uid = self.token = token
        try:
            self.decoded = jwt.decode(self.token, config.JWT_SECRET)
        except DecodeError:
            self._valid_token = False

    def is_valid(self):
        if not self._valid_token:
            return False
        for item in ['id', 'secret', 'client_id', 'scopes', 'user_key']:
            if item not in self.decoded:
                return False
        return True

    def get_grant(self):
        if not self.is_valid():
            return None
        grant_db = ndb.Key(urlsafe=self.decoded.get('id')).get()
        if grant_db and not grant_db.is_revoked and grant_db.secret == self.decoded.get('secret'):
            return grant_db
        return None

    def get_jwt(self):
        return self.token
