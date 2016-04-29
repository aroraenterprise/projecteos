"""
Project: flask-rest
Author: Saj Arora
Description: Pretty decorators to make life easy
"""
import functools

from api.v1 import errors
from auth_controller import AuthController


def auth_optional(func):
    """
    Returns UserModel if an access token is provided
    :param func:
    :return: func(user)
    """

    @functools.wraps(func)
    def decorated_function(*args, **kwargs):  # pylint: disable=missing-docstring
        user_db = AuthController.check_access_token(required=False)
        kwargs.update(dict(user=user_db))
        return func(*args, **kwargs)

    return decorated_function


def auth_required(func):
    """
    Returns UserModel with an access token
    :param func:
    :return: func(user)
    """

    @functools.wraps(func)
    def decorated_function(*args, **kwargs):  # pylint: disable=missing-docstring
        user_db = AuthController.check_access_token(required=True)
        if not user_db:
            errors.create(404, message="Account not found linked to this access token.")
        kwargs.update(dict(user=user_db))
        return func(*args, **kwargs)

    return decorated_function
