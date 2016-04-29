"""
Project: flask-rest
Author: Saj Arora
Description: Handle Email/Password authentication
"""
import base64
import json

import jwt
from google.appengine.api import urlfetch
from google.appengine.ext import ndb

import config
from api.v1.fundamentals import util
from api.v1.auth_module import AuthModel
from api.v1.auth_module.authority import AuthType

class GoogleAuth(object):

    auth_type = AuthType.GOOGLE
    _uid = ''
    CLIENT_ID = '1011559018335-3cnvdhrqe1v38dai6feptpf3j963uku9.apps.googleusercontent.com'
    CLIENT_SECRET = 'KM1z_a3pVkwDlBQR-RH6XRIR'
    REDIRECT_URI = 'http://localhost:8080'
    _parsed = {}
    _validated = False
    _is_valid = False

    def __init__(self, access_token):
        self._uid = self.access_token = access_token

    def is_valid(self): # verify signature...use google endpoint
        if self._validated:  # save parsing/request
            return self._is_valid

        self._validated = True
        url = 'https://www.googleapis.com/oauth2/v3/tokeninfo?access_token=%s' % self.access_token
        try:
            result = urlfetch.fetch(url, validate_certificate=True)
            if result.status_code == 200:
                self._parsed = data = json.loads(result.content)
                if 'aud' in data and data.get('aud') == self.CLIENT_ID and \
                                'expires_in' in data and data.get('expires_in') > 0 and 'sub' in data:
                    self._is_valid = True
                    #set uid
                    self._uid = data.get('sub')
        except:
            pass

        return self._is_valid

    def get_id(self):
        if self._is_valid:
            return base64.b64encode(str(self.auth_type) + '_' + self._uid)

    def get_key(self):
        if self._is_valid:
            return ndb.Key(AuthModel, self.get_id())

    def is_unique(self):
        auth_key = self.get_key()
        if not auth_key.get():
            return True
        return False

    def get_jwt(self):
        return jwt.encode(dict(google_id=self._uid),config.JWT_SECRET)
