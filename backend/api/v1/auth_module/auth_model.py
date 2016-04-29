"""
Project: flask-rest
Author: Saj Arora
Description: Auth model: Contains authentication data
"""
import time
from google.appengine.ext import ndb
import jwt

import config
from api.v1.fundamentals import SageModel

#################################################################################################################
# AuthModel: a container that holds a json web token with unique user credentials and links the credentials     #
# to a user account                                                                                             #
#################################################################################################################
class AuthModel(SageModel):
    user_key = ndb.KeyProperty(required=True)  # multiple auth models can have the same user_id
    auth_type = ndb.IntegerProperty(required=True, default=0)  # default is password
    jwt = ndb.StringProperty(required=True)  # stores the JWT token with all required credentials


#################################################################################################################
# GrantModel: a GRANT is a contract that provides a refresh token to a client (webapp, android, ios, etc.)      #
# Clients can exchange refresh tokens for a short-lived access tokens to gain access to various api endpoints.  #
# A grant is unique based on a specific client as identified by the client_id and the scopes requested.         #
# Once a grant is revoked by a user a                                                                           #
# client can no longer generate new access tokens from a refresh token referring to the revoked                 #
# grant and the client must re-authenticate and generate a new grant.                                           #
#################################################################################################################
class GrantModel(SageModel):
    user_key = ndb.KeyProperty(required=True)
    secret = ndb.StringProperty(required=True)
    client_id = ndb.StringProperty(required=True)
    scopes = ndb.StringProperty(default='')
    is_revoked = ndb.BooleanProperty(required=True, default=False)

    def get_refresh_token(self):
        # make sure grant model is not revoked
        if self.is_revoked:
            return None

        refresh_token = dict(
            id = self.get_key_urlsafe(),
            user_key = self.user_key.urlsafe(),
            secret = self.secret,
            scopes = self.scopes,
            client_id = self.client_id
        )
        return jwt.encode(refresh_token, config.JWT_SECRET)

    def get_access_token(self):
        # make sure grant model is not revoked
        if self.is_revoked:
            return None

        access_token = dict(
            user_key = self.user_key.urlsafe(),
            expiry = time.time() + config.ACCESS_TOKEN_EXPIRES_IN,
            scopes = self.scopes,
            client_id = self.client_id
        )
        return jwt.encode(access_token, config.JWT_SECRET)

    @classmethod
    def generate_key(cls, user_key, client_id):
        return ndb.Key(cls, 'user:' + str(user_key.id()) + '-client:' + client_id)
