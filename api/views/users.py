#!/usr/bin/python3
""" Users endpoints(routes) """
from api.views import app_views
from flask import abort
from models import storage
from models.users import User
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
