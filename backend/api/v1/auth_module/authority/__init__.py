"""
Project: flask-rest
Author: Saj Arora
Description: 
"""


## AuthType dictionary: used to identify type of authentication against which to verify
## the credentials
class AuthType(object):
    EMAIL = 0
    REFRESH_TOKEN = 1
    FACEBOOK = 2
    GOOGLE = 3


from .email_auth import *
from .refresh_token_auth import *
from .google_auth import *
