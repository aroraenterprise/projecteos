"""
Project: flask-rest
Author: Saj Arora
Description: api versions and helpers
"""

# global variables that hold the instance to the app and api
from collections import OrderedDict

from api.v1.rest import _SageRest

class SageRest(object):
    _ordered_modules = OrderedDict()
    _modules = {}
    _app = None

    @classmethod
    def start(cls, name, config, version='v1', base_url='/api/'):
        global _APP_INSTANCE, _API_INSTANCE
        cls._app = _SageRest(name, config, version, base_url)
        return cls._app
