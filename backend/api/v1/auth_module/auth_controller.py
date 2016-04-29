"""
Project: flask-rest
Author: Saj Arora
Description: Logic for authentication
"""
import time

import jwt
import pydash as _
from flask import request
from flask_restful import reqparse
from google.appengine.ext import ndb

import config
from api.v1 import errors
from api.v1.fundamentals import util, NamingConvention
from auth_model import AuthModel, GrantModel
from authority import AuthType, EmailAuth, RefreshTokenAuth, GoogleAuth


class AuthController(object):

    # naming conventions
    json_auth = 'auth'
    json_email = 'email'
    json_password = 'password'
    json_refresh_token = 'refresh_token'
    json_google_token = 'google_token'

    _all_json_names = ['json_auth', 'json_email', 'json_password',
                       'json_refresh_token', 'json_google_token']

    @classmethod
    def get_auth_module(cls):
        if cls.json_auth in request.json:
            args = _.pick(request.json.get(cls.json_auth), [cls.json_email, cls.json_password,
                                                             cls.json_refresh_token, cls.json_google_token])
            if cls.json_password in args and cls.json_email in args: # authType is password
                return EmailAuth(args.get(cls.json_email), args.get(cls.json_password))
            elif cls.json_refresh_token in args: # refresh token time
                return RefreshTokenAuth(args.get(cls.json_refresh_token))
            elif cls.json_google_token in args:
                return GoogleAuth(args.get(cls.json_google_token))
        return None

    @classmethod
    def create_unique_for_user(cls, user_key, auth_module=None):
        """
        Creates a new Auth Model if jwt is unique linked to the provided user account
        :param user_key:
        :param auth_module: Type of auth module or one is looked up in request
        :return: bool (success) True/False, string (message) auth_db/error
        """
        if not auth_module: # check for auth_module
            auth_module = cls.get_auth_module()
            if not auth_module: # check for it again...
                return False, errors.InvalidUsage(message="Invalid Credentials provided.")

        if auth_module.auth_type not in [AuthType.EMAIL, AuthType.GOOGLE]:
            return False, errors.InvalidUsage(message="Only Email/Password or Google authentication is allowed.")

        #should have an auth_module now...check for its validity and uniqueness
        if not auth_module.is_valid():
            return False, errors.InvalidUsage(message="Invalid Credentials provided.")
        if not auth_module.is_unique():
            return False, errors.InvalidUsage(message="These Credentials are already linked to an account.")

        #now auth module is valid and unique, create model and link account
        auth_db = AuthModel(
            key = auth_module.get_key(),
            auth_type = auth_module.auth_type,
            user_key = user_key,
            jwt = auth_module.get_jwt()
        )
        auth_db.put()
        return cls.authenticate_client(auth_module)

    @classmethod
    def authenticate_client(cls, auth_module=None):
        if not auth_module: # check for auth_module
            auth_module = cls.get_auth_module()
            if not auth_module: # check for it again...
                return False, errors.InvalidUsage(message ="Invalid Credentials provided.")

        #should have an auth_module now...check for its validity
        if auth_module.is_valid():
            grant_db = None
            # check if auth_module is a refresh_token
            if auth_module.auth_type == AuthType.REFRESH_TOKEN:
                grant_db = auth_module.get_grant()
            else:
                auth_db = auth_module.get_key().get()
                if auth_db: # bingo now we have a linked account
                    # create a new grant for this client
                    grant_db = cls.create_grant(auth_db, True)
                else: # valid auth module, just no user account (give a 404 error)
                    return False, errors.NotFound(message="No user account found.")
            if grant_db:
                return True, dict( # return the refresh and access tokens for the user
                    refresh_token=grant_db.get_refresh_token(),
                    access_token=grant_db.get_access_token()
                )

        return False, errors.InvalidUsage(message="Invalid Credentials. Failed to authenticate.")

    @classmethod
    @ndb.transactional
    def create_grant(cls, auth_db, save=False):
        # parse client details
        parser = reqparse.RequestParser()
        parser.add_argument('Client-Id', location='headers', required=True, dest='client_id',
                            help='Please provide Client-Id header with this request.')
        headers = parser.parse_args()

        # validate client_id
        if headers.get('client_id') not in config.CLIENT_IDS:
            errors.create(400, message="Invalid Client. Please use a valid client app to authenticate.")

        # generate a the grant_key for this client and user combination
        grant_key = GrantModel.generate_key(auth_db.user_key, headers.get('client_id'))
        grant_db = grant_key.get()
        if not grant_db:
            # create grant
            grant_db = GrantModel(
                key = grant_key,
                user_key = auth_db.user_key,
                secret = util.uuid(),
                client_id = headers.get('client_id')
            )
            if save:
                grant_db.put()
        return grant_db

    @classmethod
    def check_access_token(cls, required=True):
        parser = reqparse.RequestParser()
        parser.add_argument('Client-Id', location='headers', required=True, dest='client_id',
                            help='Please provide Client-Id header with this request.')
        parser.add_argument('Bearer', location='headers', required=required, dest='bearer',
                            help='Please provide a Bearer header with the access token to reach this endpoint.')
        headers = parser.parse_args()

        # validate client_id
        if headers.get('client_id') not in config.CLIENT_IDS:
            errors.create(400, message="Invalid Client. Please use a valid client app to authenticate.")

        if 'bearer' not in headers or not headers.get('bearer'):
            if required:
                errors.create(401, message="Missing access token. Please provide a Bearer header with this request.")
            else:
                return None

        # there is a access token provided, lets process it
        invalid_token_error = errors.Unauthorized(message="Invalid access token. Use a refresh token or re-authenticate.")
        try:
            decoded_token = jwt.decode(headers.get('bearer'), config.JWT_SECRET)
            # check that all properties are present in the decoded token
            for item in ['scopes', 'expiry', 'client_id', 'user_key']:
                if item not in decoded_token:
                    raise invalid_token_error

            # check client id in access_token against current header client_id and expiry
            if headers.get('client_id') != decoded_token.get('client_id') or time.time() > decoded_token.get('expiry'):
                raise invalid_token_error

            # access token is good to use
            user_db = ndb.Key(urlsafe=decoded_token.get('user_key')).get()
            return user_db

        except:
            pass
        raise invalid_token_error




