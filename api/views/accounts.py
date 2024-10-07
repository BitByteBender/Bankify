#!/usr/bin/python3
""" Accounts endpoints(routes) """

from api.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.users import User
from models.accounts import Account
from sqlalchemy.exc import IntegrityError
from uuid import uuid4
import json


USR_PATH = '/users/<user_id>'
ACC_PATH = '/accounts'
ACC_ID_PATH = str(ACC_PATH + '/<account_id>')
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


@app_views.route(ACC_ID_PATH, methods=['GET'], strict_slashes=False)
def get_single_account(account_id):
    """ Retrieves a specifc accoung based on its id """
    acc_rec = storage.get(Account, account_id) or abort(404)
    return (json.dumps(acc_rec.to_dict(), indent=4) + '\n', 200)


@app_views.route(UA_PATH, methods=['POST'], strict_slashes=False)
def insert_account(user_id):
    """ Inserts a new bank account for a specific user """
    user_obj = storage.get(User, user_id) or abort(404)
    data = request.get_json() or abort(400, "Not a JSON")
    balance = data.get('balance') if 'balance' in data else abort(400, "Balance is missing")
    credits = data.get('credits') if 'credits' in data else abort(400, "Credits is missing")
    on_hold = data.get('on_hold', False)

    data.update({
        'id': str(uuid4()),
        'user_id': user_id,
        'balance': str(balance),
        'credits': str(credits),
        'on_hold': on_hold,
    })

    try:
        new_account = Account(**data)
        print("New account record: ", new_account)
        storage.new(new_account)
        storage.save()
    except IntegrityError as ie:
        print("IntegrityError: ", ie)
        storage.rollback()
        abort(400, "Duplicate entry")
    except Exception as e:
        print("Exception: ", e)
        storage.rollback()
        abort(500, "Failed to insert a new account due to databassse constraint violation")
    return (json.dumps(new_account.to_dict()) + '\n', 201)


@app_views.route(ACC_ID_PATH, methods=['PUT'], strict_slashes=False)
def updates_account(account_id):
    """ Updates a specific Account record by id """
    account_obj = storage.get(Account, account_id) or abort(404, "Account not found")
    data = request.get_json() or abort(400, "Not a JSON")
    key_fields = {'id', 'user_id', 'created_at', 'updated_at'}
    [setattr(account_obj, key, value) for key, value in data.items()
        if key not in key_fields]
    storage.save()
    return (json.dumps(account_obj.to_dict(), indent=3) + '\n', 200)


@app_views.route(ACC_ID_PATH, methods=['DEL'], strict_slashes=False)
def deletes_account_record(account_id):
    """ Deletes a specific Account record by id """
    acc_obj = storage.get(Account, account_id) or abort(404, "Account not found")
    try:
        storage.delete(acc_obj)
        storage.save()
        return (jsonify({}), 200)
    except Exception as e:
        return (jsonify({"Error": str(e)}), 500)
