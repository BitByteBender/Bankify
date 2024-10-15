#!/usr/bin/env python3

from api.views import app_views, transactions_bp
from flask import Flask, jsonify, render_template, session, redirect, url_for, request
from flask_cors import CORS
from flask_session import Session
from models import storage
from models.users import User
from os import getenv
from api.auth import auth_bp
import os


app = Flask(__name__, static_folder='../static', template_folder='../templates');
CORS(app)
app.config['SECRET_KEY'] = getenv('SECRET_KEY', os.urandom(24))
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './flask_session/'
app.config['SESSION_PERMANENT'] = False
Session(app)

app.register_blueprint(app_views, url_prefix='/api')
app.register_blueprint(auth_bp, transactions_bp, url_prefix='/api')


def obfuscate_id(user_id):
    """ obfuscation (reverse and shift characters) """
    obfuscated = ''.join(chr(ord(c) + 3) for c in user_id[::-1])
    return obfuscated


def deobfuscate_id(obfuscated_id):
    """ Reverse the obfuscation """
    user_id = ''.join(chr(ord(c) - 3) for c in obfuscated_id[::-1])
    return user_id


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile_page():
    """ Renders profile_page """
    if 'user_id' not in session:
        return redirect(url_for('authentication_page'))
    return render_template('profile.html', user_id=session['user_id'])


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


@app.route('/dashboard/manager/users', methods=['GET'], strict_slashes=False)
def dashboard_users_list():
    """Renders the dashboard users list page"""
    if not session.get('is_admin'):
        return redirect(url_for('auth_bp.dashboard_login_page'))
    return render_template('dashboard_users_list.html')


@app.route('/dashboard/manager/update=user_id', methods=['GET'], strict_slashes=False)
def update_user_page():
    """
        Renders the update user page
        Get the obfuscated ID from the URL
        Deobfuscate the ID
    """
    if not session.get('is_admin'):
        return redirect(url_for('auth_bp.dashboard_login_page'))

    obfuscated_id = request.args.get('id')
    if not obfuscated_id:
        return jsonify({"error": "User ID not found in URL"}), 400

    user_id = deobfuscate_id(obfuscated_id)
    user = storage.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return render_template('update_user.html', user=user)


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
