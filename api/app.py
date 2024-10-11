#!/usr/bin/env python3

from api.views import app_views
from flask import Flask, jsonify, render_template, session, redirect, url_for, request
from flask_cors import CORS
from flask_session import Session
from models import storage
from os import getenv
from api.auth import auth_bp
import os


app = Flask(__name__, template_folder='../templates');
CORS(app)
app.config['SECRET_KEY'] = getenv('SECRET_KEY', os.urandom(24))
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './flask_session/'
app.config['SESSION_PERMANENT'] = False
Session(app)

app.register_blueprint(app_views, url_prefix='/api')
app.register_blueprint(auth_bp)


@app.before_request
def check_if_logged_in():
    """
    Redirect the user if they are trying to access login or register pages while logged in.
    List of routes the user should be redirected from when logged in
    """
    restricted_routes = ['/login', '/register']

    if 'user_id' in session and request.path in restricted_routes:
        return redirect(url_for('home_page'))


@app.route('/dashboard', methods=['GET'], endpoint='dashboard_home')
def dashboard_home():
    """Renders the dashboard page"""
    if not session.get('is_admin'):
        return redirect(url_for('auth_bp.dashboard_login_page'))
    return render_template('dashboard.html')


@app.route('/', methods=['GET'])
def authentication_page():
    """ Renders the landing page with login and registration options """
    if 'user_id' in session:
        return redirect(url_for('home_page'))
    return render_template('authentication.html')


@app.route('/register', methods=['GET'], strict_slashes=False)
def register():
    """ Serve the registration form """
    if 'user_id' in session:
        return redirect(url_for('home_page'))
    return render_template('register.html')


@app.route('/login', methods=['GET'], strict_slashes=False)
def login_page():
    """ Renders the login form """
    if 'user_id' in session:
        return redirect(url_for('home_page'))
    return render_template('login.html')

@app.route('/logout', methods=['GET'], strict_slashes=False)
def logout():
    """Logs out the user by clearing the session."""
    session.clear()
    return redirect(url_for('authentication_page'))


@app.route('/dashboard/logout', methods=['GET'], strict_slashes=False)
def dashboard_logout():
    """Logs out the user by clearing the session."""
    session.clear()
    return redirect(url_for('auth_bp.dashboard_login_page'))


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'], strict_slashes=False)
def home_page():
    """ Renders home_page """
    if 'user_id' not in session:
        return redirect(url_for('authentication_page'))
    return render_template('home.html')


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
