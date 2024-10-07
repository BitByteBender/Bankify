from flask import Blueprint, jsonify, request
from models.engine.db_storage import DBStorage
from models.users import User

users_manager = Blueprint('users_manager', __name__)
storage = DBStorage()  # Initialize the storage engine

@users_manager.route('/users', methods=['GET'])
def get_users():
    """Retrieve all users or a specific user by ID."""
    user_id = request.args.get('user_id')
    if user_id:
        user = storage.get(User, user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user.to_dict()), 200

    users = storage.all(User)
    user_list = [user.to_dict() for user in users.values()]
    return jsonify(user_list), 200

@users_manager.route('/users', methods=['POST'])
def create_user():
    """Create a new user."""
    data = request.get_json()
    if not data or not all(k in data for k in ('full_name', 'email', 'password', 'phone', 'address')):
        return jsonify({"error": "Missing data"}), 400

    user = User(**data)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201

@users_manager.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update an existing user."""
    user = storage.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    for key, value in data.items():
        setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200

@users_manager.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user."""
    user = storage.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    storage.delete(user)
    storage.save()
    return jsonify({"success": "User deleted"}), 200
