#!/usr/bin/python3
""" Users endpoints(routes) """
from api.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.users import User
from sqlalchemy.exc import IntegrityError
from uuid import uuid4
import json


PATH = '/users'


@app_views.route(PATH, methods=['GET'], strict_slashes=False)
def get_all_users():
    """ Retrieves the list of all Users objects """
    user_records = storage.all(User).values()
    return (json.dumps([usr.to_dict() for usr in user_records], indent=4) + '\n')


@app_views.route(PATH + '/<user_id>', methods=['GET'], strict_slashes=False)
def get_single_user(user_id):
    """ Retrives a single User object basedd on its id """
    return (json.dumps(storage.get(User, user_id).to_dict(), indent=2)
            + '\n' if storage.get(User, user_id) else abort(404))


@app_views.route(PATH, methods=['POST'], strict_slashes=False)
def insert_user_record():
    """ Inserts a new User into the database """
    data = request.get_json() or abort(400, "Not a JSON")
    first_name = data.get('first_name') or abort(400, "First name is missing")
    last_name = data.get('last_name') or abort(400, "Last name is missing")
    phone = data.get('phone') or abort(400, "Phone number is missing")
    email = data.get('email') or abort(400, "Email is missing")
    password = data.get('password') or abort(400, "Password is missing")
    address = data.get('address') or abort(400, "Address is missing")
    account_activation_status = data.get('acc_activation', False)
    is_admin = data.get('is_admin', False)

    data.update({
        'id': str(uuid4()),
        'full_name': str(first_name + " " + last_name),
        'phone': phone,
        'email': email,
        'password': password,
        'address': address,
        'account_activation_status': account_activation_status,
        'is_admin': is_admin,
    })

    try:
        new_user = User(**data)
        print("New user record: ", new_user)
        storage.new(new_user)
        storage.save()
    except IntegrityError as ie:
        print("IntegrityError: ", ie)
        storage.rollback()
        abort(400, "Duplicatte entry")
    except Exception as e:
        print("Exception: ", e)
        storage.rollback()
        abort(500, "Failed to insert a new user due to database constraint violation")
    return (json.dumps(new_user.to_dict()) + '\n', 201)


@app_views.route(PATH + '/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user_record(user_id):
    """ Updates a User record """
    user_obj = storage.get(User, user_id) or abort(404, "User not found")
    data = request.get_json() or abort(400, "Not a JSON")
    key_fields = {'id', 'created_at', 'updated_at'}
    [setattr(user_obj, key, value) for key, value in data.items()
        if key not in key_fields]
    storage.save()
    return (json.dumps(user_obj.to_dict(), indent=3) + '\n', 200)


@app_views.route(PATH + '/<user_id>', methods=['DEL'], strict_slashes=False)
def delete_user_record(user_id):
    """ Deleted a User record """
    user_obj = storage.get(User, user_id) or abort(404, "User not found")
    try:
        storage.delete(user_obj)
        storage.save()
        return (jsonify({}), 200)
    except Exception as e:
        return (jsonify({"Error": str(e)}), 500)
