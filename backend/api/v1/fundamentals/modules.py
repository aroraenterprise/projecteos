"""
Project: flask-rest
Author: Saj Arora
Description: A Modular approach that allows dependency injections based on enabled
modules and their dependencies
"""
from api.v1.fundamentals import SageString, SageGravatar


class Module(object):
    def __init__(self, name, imports, dependencies=None):
        self.name = name
        self._imports = imports
        self._dependencies = dependencies or []

    def link(self, api, **kwds):
        module = map(__import__, self._imports)

    def get_dependencies(self):
        return self._dependencies
