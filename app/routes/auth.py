from flask import Blueprint, request, jsonify
from app.services.user_service import create_user, authenticate_user

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register_user():
    data = request.json
    result = create_user(data)
    return jsonify(result), result.get('status', 400)

@auth.route('/login', methods=['POST'])
def login_user():
    data = request.json
    result = authenticate_user(data)
    return jsonify(result), result.get('status', 400)