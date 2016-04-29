"""
Project: athena-server
Author: Saj Arora
Description: 
"""
from api.v1 import SageController, SageMethod, make_json_ok_response


def sage_account_me_function(self, account, **kwargs):
    return account.to_dict()

def sage_account_update_function(self, key, resource, **kwargs):
    return make_json_ok_response(dict(method="update"))


account_controller = {
    'me': SageController(sage_account_me_function),
    '': SageController(sage_account_me_function),
    '<string:key>':[
        SageController(sage_account_update_function, SageMethod.PUT)
    ]
}