"""
Project: flask-rest
Author: Saj Arora
Description: Fabricated modules
"""
from api.v1 import Module, SageResource, SageString, SageGravatar, SageInteger, SageDateTime, SageController, SageMethod
from api.v1.account_module import account_api
from api.v1.auth_module import auth_api, AuthController
from api.v1.fundamentals import util


class SageAccountModule(SageResource):
    """
    A user module that can be initialized easily and linked with SageAuthModule
    """
    _default_model_dict = {
        "email": SageString(validator_name='email', required=True)
    }

    _default_validator_dict = {
        "email": util.EMAIL_REGEX
    }

    def __init__(self, name='accounts', model_dict=None, validator_dict=None, uid='sage.account_module',
                 controllers=None):
        model_dict = model_dict or self._default_model_dict
        validator_dict = validator_dict or self._default_validator_dict
        controllers = controllers or account_api.account_controller
        super(SageAccountModule, self).__init__(uid, name, None,
                                                [], model_dict,
                                                validator_dict,
                                                controllers)


class SageAuthModule(SageResource):
    """
    An authentication module that instantiates all endpoints for authentication,
    signing up, etc.
    """
    def __init__(self, user_module, uid='sage.auth_module', name='auth'):
        if not isinstance(user_module, SageAccountModule):
            raise Exception("UserModule for SageAuthModule must inherit from SageUserModule.")
        super(SageAuthModule, self).__init__(uid, name)
        self._account_module = user_module
        self.controllers = auth_api.auth_controller

    def get_account_model(self):
        return self._account_module.get_model()

    def authenticate(self, required=True):
        return AuthController.check_access_token(required)