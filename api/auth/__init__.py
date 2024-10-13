#!/usr/bin/python3
from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from api.auth.login import login
from api.auth.utils import forgot_password, reset_password


auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def handle_login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        return login()


@auth_bp.route('/dashboard/login', methods=['GET'], strict_slashes=False)
def dashboard_login_page():
    if session.get('is_admin'):
        return redirect(url_for('dashboard_home'))
    return render_template('dashboard_login.html')


@auth_bp.route('/dashboard/login', methods=['POST'], strict_slashes=False)
def dashboard_login():
    return login()


@auth_bp.route('/forgot_password', methods=['GET', 'POST'], strict_slashes=False)
def handle_forgot_password():
    return forgot_password()


@auth_bp.route('/reset_password', methods=['GET', 'POST'], strict_slashes=False)
def handle_reset_password():
    if request.method == 'GET':
        return render_template('reset_password.html')
    return reset_password()
