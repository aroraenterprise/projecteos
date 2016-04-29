#!/usr/bin/env python
#
"""
Project: Project-Eos
Author: Saj Arora
Description: Open Data platform for research, predictive data analytics and bridging
scienctific community and non-researchers to drive a unified frontier in science, exploration and discovery
"""
import flask

from api import SageRest
import config

# start the app
from api.v1 import SageString, SageDateTime, SageResource, SageInteger, SageBool, SageGravatar

app = SageRest.start(__name__, config)


## HOME PAGE: List all dataset
@app.route('/')
def index():
    """
    Gets all the datasets and lists them with their endpoints
    :return:
    """
    print 'hello'
    return flask.jsonify(dict(works=True))


from dataset_module import dataset_module
app.add_modules([dataset_module])


@app.after_request
def add_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response
