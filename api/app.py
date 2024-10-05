#!/usr/bin/env python3

from flask import Flask, jsonify, session
from models import storage
from api.views import app_views
from os import getenv


app = Flask(__name__);

app.register_blueprint(app_views)


@app.errorhandler(404)
def trigger_error(err):
    """ Triggers a 404 error """
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown_db(exception):
    """ Close storage on teardown """
    storage.close()


if __name__ == '__main__':
    """ Runs flask app on a specified adr and port """
    host = getenv('BK_API_HOST', '0.0.0.0')
    port = int(getenv('BK_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True, debug=True)
