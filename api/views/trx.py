#!/usr/bin/python3
""" Transactions endpoints(routes) """

from api.views import app_views
from models import storage
from models.trx import Transaction
import json

TRX_PATH = '/trx'

@app_views.route(TRX_PATH, methods=['GET'], strict_slashes=False)
def get_all_system_trx():
    """ Retrieves all Transactions records in the system """
    trx_objs = storage.all(Transaction).values()
    return (json.dumps([trx.to_dict() for trx in trx_objs], indent=3) + '\n')
