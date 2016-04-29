"""
Project: flask-rest
Author: Saj Arora
Description: 
"""
import logging

import flask
import flask_restful as restful

from api.v1 import errors


class Api(restful.Api):  # pylint: disable=too-few-public-methods
    """By extending restful.Api class we can make custom implementation of some of its methods"""

    def __init__(self, app, version, base_url):
        super(Api, self).__init__(app)
        self._version = version
        self._base_url = base_url + version + '/'

    def get_name(self, endpoint=None):
        """
        Gets name for endpoint in v1 api
        :param endpoint: name of endpoint
        :return: full path to endpoint
        """
        if not endpoint:
            return self._version
        else:
            return self._base_url + endpoint

    def handle_error(self, err):
        """Specifies error handler for REST API.
        It is called when exception is raised during request processing

        Args:
            err (Exception): the raised Exception object

        """
        return handle_error(err)


def handle_error(err):
    """This error handler logs exception and then makes response with most
    appropriate error message and error code

    Args:
        err (Exception): the raised Exception object

    """
    logging.exception(err)
    message = ''
    if hasattr(err, 'data') and err.data['message']:
        message = err.data['message']
    elif hasattr(err, 'message') and err.message:
        message = err.message
    elif hasattr(err, 'description'):
        message = err.description
    try:
        err.code
    except AttributeError:
        err.code = 500

    if isinstance(err, errors.ApiException):
        response = flask.jsonify(err.to_dict())
        response.status_code = err.status_code
        return response, err.status_code
    else:
        return flask.jsonify({
            'message': message
        }), err.code
