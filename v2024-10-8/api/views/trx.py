#!/usr/bin/python3
""" Transactions endpoints(routes) """

from api.views import app_views
from flask import abort
from models import storage
from models.accounts import Account
from models.trx import Transaction
import json


TRX_PATH = '/trx'
ACC_PATH = '/accounts/<account_id>'


@app_views.route(TRX_PATH, methods=['GET'], strict_slashes=False)
def gets_all_system_trx():
    """ Retrieves all Transactions records in the system """
    trx_objs = storage.all(Transaction).values()
    return (json.dumps([trx.to_dict() for trx in trx_objs], indent=3) + '\n')


@app_views.route(ACC_PATH + TRX_PATH, methods=['GET'], strict_slashes=False)
def gets_all_acc_trx(account_id):
    """ Retrieves all Transactions done by a specific account """
    acc_obj = storage.get(Account, account_id) or abort(404)
    acc_trx = acc_obj.sent_transactions + acc_obj.received_transactions
    return (json.dumps([trx.to_dict() for trx in acc_trx],
            indent=3) + '\n', 200)
