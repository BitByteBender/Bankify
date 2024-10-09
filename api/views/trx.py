#!/usr/bin/python3
""" Transactions endpoints(routes) """

from api.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.accounts import Account
from models.trx import Transaction, TransactionStatus
from decimal import Decimal
from datetime import datetime
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
    """ Retrieves all Transactions done by a specific account as a sender or receiver """
    acc_obj = storage.get(Account, account_id) or abort(404)
    
    sent_transactions = acc_obj.sent_transactions
    received_transactions = acc_obj.received_transactions
    
    trx_to_return = []
    
    if sent_transactions:
        trx_to_return.extend(
            trx.to_dict() for trx in sent_transactions if trx.status == TransactionStatus.SENT
        )
        
    if received_transactions:
        trx_to_return.extend(
            trx.to_dict() for trx in received_transactions if trx.status == TransactionStatus.RECEIVED
        )
    
    if not trx_to_return:
        return jsonify({"message": "No transactions found for this account"}), 200
    
    return jsonify(trx_to_return), 200


@app_views.route(TRX_PATH, methods=['POST'], strict_slashes=False)
def create_trx():
    """ Creates a new transaction """
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    required_fields = ['sender_id', 'receiver_id', 'amount', 'status']
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")

    sender_account = storage.get(Account, data['sender_id'])
    receiver_account = storage.get(Account, data['receiver_id'])
    
    if not sender_account and data['status'] != 'DEPOSIT':
        abort(404, description="Sender account not found")
    
    if not receiver_account and data['status'] != 'WITHDRAW':
        abort(404, description="Receiver account not found")

    if data['status'] == "SENT":
        amount = Decimal(data['amount'])
        if sender_account.balance < amount:
            abort(400, description="Insufficient funds in sender's account")

        sender_account.balance -= amount
        receiver_account.balance += amount

    trx_sender = Transaction(
        sender_id=data['sender_id'],
        receiver_id=data['receiver_id'],
        amount=float(data['amount']),
        status=TransactionStatus.SENT,
        transaction_date=data.get('transaction_date', datetime.now())
    )
    
    storage.new(trx_sender)

    if data['status'] == "SENT":
        trx_receiver = Transaction(
            sender_id=data['sender_id'],
            receiver_id=data['receiver_id'],
            amount=float(data['amount']),
            status=TransactionStatus.RECEIVED,
            transaction_date=data.get('transaction_date', datetime.now())
        )
        storage.new(trx_receiver)
    storage.save()

    return jsonify(trx_sender.to_dict()), 201
