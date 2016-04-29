"""
Project: backend
Author: Saj Arora
Description: Tasks helper (background workers)
"""
import dataset_processor
from main import app
from flask import request
import json

@app.route('/tasks/<name>', methods=['POST'])
def run_task(name):
    callable = dict()
    for fxn in dataset_processor.fxns:
        callable[fxn.get('name')] = fxn.get('value')

    if name in callable:
        if request.data:
            data = json.loads(request.data)
            callable.get(name)(**data)

    return 'ok'