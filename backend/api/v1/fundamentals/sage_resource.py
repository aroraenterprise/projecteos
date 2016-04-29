"""
Project: flask-rest
Author: Saj Arora
Description: 
"""
from flask_restful import Resource

from .model import SageModel
from .validator import SageValidator
from .sage_controller import SageController, get_default_controllers
from .sage_methods import SageMethod
from .modules import Module

class SageResource(Module):
    ALL = SageController.ALL
    ONE = SageController.ONE
    _model = None
    _validator = None
    _behind_authentication = None
    _default_endpoints = {
        ALL: [SageMethod.GET, SageMethod.POST],
        ONE: [SageMethod.GET, SageMethod.PUT, SageMethod.DELETE]
    }

    def __init__(self, uid, name,
                 within_uid=None,  # uid of resource this resource belongs to
                 dependencies=None,
                 # (e.g. users/123/pictures: pictures is inside users resource)
                 model_dict=None, # dictionary with all the model properties
                 validator_dict=None, # dictionary with all the validator properties
                 endpoints=None,
                 controllers=None, # array of instances of SageController class
                 authenticate=True
                 ):
        super(SageResource, self).__init__(uid, [], dependencies) # no imports needed
        self._auth_module = None
        self.uid = uid
        self.name = name
        self.within_uid = within_uid
        self.model_dict = model_dict
        self.validator_dict = validator_dict
        self.endpoints = endpoints or self._default_endpoints
        self.controllers = self.create_controllers(self.endpoints, controllers)
        self.dependencies = dependencies or []
        self._behind_authentication = authenticate

    def create_controllers(self, endpoints, controllers):
        result = {}
        default_controllers = get_default_controllers(self.name)
        for type, endpoints in endpoints.iteritems():
            # figure out url based on type (all or one)
            _type = '' if type == self.ALL else '<string:%skey>' % self.name
            if _type not in result:
                result[_type] = []

            if not isinstance(endpoints, list):
                endpoints = [endpoints]

            for endpoint in endpoints:
                controller = None
                # get controller from assigned or default controllers
                if controllers and type + endpoint in controllers: # e.g. allget
                    controller = controllers.get(type + endpoint)
                else:
                    controller = default_controllers.get(type + endpoint)

                if controller:
                    result[_type].append(controller)
        return result

    # override the module link to actually build the resource
    def link(self, api, **kwds): # builds the resource
        self._auth_module = kwds.get('auth', None)
        self._build(api)

    def requires_authentication(self):
        return self._behind_authentication

    def _build(self, api):
        # build validator
        validator = self._build_validator()

        # build models
        model = self._build_model(validator)



        # create controllers and then api endponts
        self._build_endpoints(api)

    def _build_endpoints(self, api):
        """
        Builds controllers and endpoints for this resource (e.g. Create a User or List Users or Get one User by key)
        :param api:
        :return:
        """
        # create controllers
        for endpoint, controller_list in self.controllers.iteritems(): # iterate over grouping of endpoints to make a new api.resource
            controllers = dict()
            if not isinstance(controller_list, list):
                controller_list = [controller_list]

            for controller in controller_list:
                # add this resource to controller to allow access to model
                controllers[controller.method] = controller.get_fxn(self)

            # link controller to endpoints
            if endpoint != '': # no custom endpoint
                api_class = type('Resource%s%sApi' % (self.name.capitalize(), endpoint.capitalize()),
                                 (Resource,), controllers)
                api.add_resource(api_class, api.get_name('%s/%s' % (self.name, endpoint)))
            else:
                api_class = type('Resource%sApi' % self.name.capitalize(), (Resource,), controllers)
                api.add_resource(api_class, api.get_name('%s' % self.name))

    def _build_model(self, validator=None):
        if self.model_dict:
            self.model_dict['validator'] = validator
            self._model = type('%sModel' % self.name.capitalize(), (SageModel,), self.model_dict)
        return self.get_model()

    def _build_validator(self):
        if self.validator_dict:
            return type('%sValidator' % self.name.capitalize(),
                                   (SageValidator,), self.validator_dict)
        return None

    def get_model(self):
        """
        Returns the model class for this resource
        but if no model then returns the SageModel class
        :return:
        """
        return self._model or SageModel
    
    def get_auth(self):
        return self._auth_module
