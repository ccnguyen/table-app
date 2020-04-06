import time
import os
from flask import Flask
from flask_restful import Resource, Api
from flask_pymongo import PyMongo
from flask import make_response
from bson.json_util import dumps

MONGO_URL = os.environ.get('MONGO_URL')
if not MONGO_URL:
    MONGO_URL = "mongodb://localhost:27017/rest";

app = Flask(__name__, static_folder='build', static_url_path='/')
app.config['MONGO_URI'] = MONGO_URL
mongo = PyMongo(app)

def output_json(obj, code, headers=None):
    resp = make_response(dumps(obj), code)
    resp.headers.extend(headers or {})
    return resp

DEFAULT_REPRESENTATIONS = {'application/json': output_json}

api = Api(app)
api.representations = DEFAULT_REPRESENTATIONS

@app.route('/')
def index():
	return app.send_static_file('index.html')

@app.route('/api/time')
def get_current_time():
	return {'time': time.time()}

import flask_rest_service.resources