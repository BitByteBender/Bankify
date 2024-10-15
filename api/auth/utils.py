#!/usr/bin/python3
from flask import request, session, jsonify, render_template
from models.users import User
from models import storage
# from werkzeug.security import generate_password_hash


def forgot_password():
    """ Checks if the email exists in the database
        Stores the email in the session for the reset_password function
    """
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Missing JSON data"}), 400

    email = data.get('email')

    user = storage._DBStorage__session.query(User).filter_by(email=email).first()
    
    if not user:
        return jsonify({"error": "Email not found"}), 404

    session['reset_email'] = email  
    return jsonify({"message": "Proceed to reset password page"}), 200


def reset_password():
    """
        Retrieves the email from the session
        Clears the reset_email from the session after successful reset
    """
    data = request.get_json()
    
    if data is None:
        return jsonify({"error": "Missing JSON data"}), 400

    new_password = data.get('password')
    
    if not new_password:
        return jsonify({"error": "New password is required"}), 400

    email = session.get('reset_email') 
    if not email:
        return jsonify({"error": "Email not found in session"}), 400

    user = storage._DBStorage__session.query(User).filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.password = new_password 
    storage._DBStorage__session.commit()

    session.pop('reset_email', None)  
    return jsonify({"message": "Password reset successful", "redirect": "/login"}), 200
