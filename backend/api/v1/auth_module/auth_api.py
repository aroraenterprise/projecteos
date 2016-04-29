"""
Project: flask-rest
Author: Saj Arora
Description: Handle auth endpoints such as auth/signup, auth/login
"""
from api.v1 import make_json_ok_response, SageController, SageMethod
from api.v1.fundamentals import helper
from .auth_controller import AuthController


def sage_auth_signup_function(self, resource, **kwargs):
    _UserModel = resource.get_account_model()
    args = helper.parse_args_for_model(_UserModel)
    user = _UserModel(**args)  # user has been created
    user.put()  # save to get a key for the user

    result, params = AuthController.create_unique_for_user(user.key)
    if not result:  # not successful
        user.key.delete()
        raise params  # this holds the error message
    else:
        return params  # this holds accesskey and refresh token


def sage_auth_authenticate_function(self, resource, **kwargs):
    result, params = AuthController.authenticate_client()
    if not result:  # not successful
        raise params  # this holds the error message
    else:
        return params  # this holds the refresh token and the access token


auth_controller = {
    'signup': SageController(sage_auth_signup_function, SageMethod.POST, authenticate=False),
    'authenticate': SageController(sage_auth_authenticate_function, SageMethod.POST, authenticate=False)
}