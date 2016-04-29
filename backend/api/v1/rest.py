"""
Project: flask-rest
Author: Saj Arora
Description: Initializes the rest app
"""
from collections import OrderedDict

import flask

from api.v1 import Api


class _SageRest(flask.Flask):
    _api = None
    __modules = []
    _modules = {}
    _ordered_modules = OrderedDict()
    _auth_module = None

    def __init__(self, name, config, version, base_url):
        super(_SageRest, self).__init__(name)
        self.name = name
        self.config.from_object(config or {})
        # init flask_restful
        self._api = Api(self, version, base_url)

    def get_api(self):
        return self._api

    def set_auth(self, auth_module):
        self._auth_module = auth_module
        self.__modules.append(auth_module)
        
    def add_modules(self, modules=None):
        modules = self.__modules + modules or []
        for module in modules:
            self._modules[module.name] = module

        self._sort_module_dependencies()
        for name, module in self._ordered_modules.iteritems():
            module.link(self.get_api(), auth=self._auth_module)

    def _sort_module_dependencies(self):
        for module_name, module in self._modules.iteritems():
            if module_name in self._ordered_modules: # already loaded dependencies for this module
                continue

            self._load_dependencies(module)
            # add to ordered modules list
            self._ordered_modules[module_name] = module

    def _load_dependencies(self, module, dependent_modules=None):
        dependent_modules = dependent_modules or []

        for dependency_name in module.get_dependencies():
            # fetch the dependency:
            if not dependency_name in self._modules:
                raise Exception('%s module not found as an import for this app. Please create or register '
                                'this module during intialization to continue.' % dependency_name)
            dependency = self._modules.get(dependency_name)

            if dependency.name in self._ordered_modules:  # already loaded, awesome
                continue

            # check for circular depencies
            if dependency_name in dependent_modules:
                raise Exception('%s is a dependency of %s which in turn '
                                'itself is a dependency of %s. Please fix this circular '
                                'dependency.' % (
                                    dependency_name, module.name, dependency_name
                                ))

            # not a circular dependency, add current dependency to the dependent_modules
            _dependent_modules = dependent_modules or [] + [dependency.name]
            # load all dependencies of the current dependency
            self._load_dependencies(dependency, _dependent_modules)

            # add to ordered modules list
            self._ordered_modules[dependency.name] = dependency