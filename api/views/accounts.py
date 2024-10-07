#!/usr/bin/python3
""" Accounts endpoints(routes) """

from api.views import app_views
from flask import abort
from models import storage
from models.users import User
from models.accounts import Account
import json


USR_PATH = '/users/<user_id>'
ACC_PATH = '/accounts'
ACCID_PATH = str(ACC_PATH + '/<account_id>')
UA_PATH = str(USR_PATH + ACC_PATH)


@app_views.route(ACC_PATH, methods=['GET'], strict_slashes=False)
def get_all_accounts():
    """ Retrieves all bank accounts """ 
    acc_records = storage.all(Account).values()
    return (json.dumps([acc.to_dict() for acc in acc_records], indent=4) + '\n')


@app_views.route(UA_PATH, methods=['GET'], strict_slashes=False)
def get_all_user_accounts(user_id):
    """ Retrieves all Accounts specific to a User """
    user_record = storage.get(User, user_id) or abort(404, "Not found")
    return (json.dumps([usr.to_dict() for usr in user_record.accounts],
            indent=4) + '\n', 200)


@app_views.route(ACCID_PATH, methods=['GET'], strict_slashes=False)
def get_single_account(account_id):
    """ Retrieves a specifc accoung based on its id """
    acc_rec = storage.get(Account, account_id) or abort(404)
    return (json.dumps(acc_rec.to_dict(), indent=4) + '\n', 200)
