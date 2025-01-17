#!/usr/bin/python3
""" api entry point """
from flask import Flask
from flask import make_response
from flask import jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv
from os import environ


HBNB_API_HOST = getenv('HBNB_API_HOST') if environ.get(
    'HBNB_API_HOST') else '0.0.0.0'
HBNB_API_PORT = getenv('HBNB_API_PORT') if environ.get(
    'HBNB_API_PORT') else '5000'

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(err):
    """a function exectue when a request finshed"""
    storage.close()


@app.errorhandler(404)
def error404(err):
    """handel 404 error"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
