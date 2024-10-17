#!/usr/bin/env python3
from flask import Flask, jsonify, request, abort, session, redirect, url_for
from models import storage
from models.users import User


def login():
    """
        Handle user login
        Get JSON data from the request body
        Handle the case where JSON is not provided
        Retrieve email & password from JSON data
        Query the user by email using the existing session
        Simple password comparison since the passwords are not hashed
        Check if the user is trying to log in as admin (/dashboard/login)
        If admin, allow access to the dashboard
    """
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Missing JSON data"}), 400

    email = data.get('email')
    password = data.get('password')

    # print the captured email and password > Debugging Line
    print("Email: {}, Password: {}".format(email, password))

    user = storage._DBStorage__session.query(User).filter_by(email=email).first()

    if user and user.password == password:
        if request.path == '/dashboard/login':
            if not user.is_admin:
                return jsonify({"error": "Access denied: Admins only"}), 403

            session['user_id'] = user.id
            session['is_admin'] = True
            return jsonify({"success": "Admin login successful", "redirect": "/dashboard"}), 200
        else:
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            return jsonify({"success": "Login successful", "redirect": "/home"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401
