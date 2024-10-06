from flask import Blueprint, jsonify, request
from models.trx import Transaction
from models.accounts import Account
from models.engine.db_storage import DBStorage

trx_handler = Blueprint('trx_handler', __name__)

@trx_handler.route('/transactions', methods=['POST'])
def create_transaction():
    data = request.get_json()
    sender_id = data.get('sender_id')
    receiver_id = data.get('receiver_id')
    amount = data.get('amount')

    sender_account = DBStorage.get(Account, sender_id)
    receiver_account = DBStorage.get(Account, receiver_id)

    if not sender_account or not receiver_account:
        return jsonify({"error": "Invalid account ID"}), 400
    
    if sender_account.balance < amount:
        return jsonify({"error": "Insufficient funds"}), 400

    transaction = Transaction(sender_id=sender_id, receiver_id=receiver_id, amount=amount)
    DBStorage.new(transaction)
    DBStorage.save()

    return jsonify(transaction.to_dict()), 201

@trx_handler.route('/transactions/<user_id>', methods=['GET'])
def get_user_transactions(user_id):
    transactions = DBStorage.all(Transaction)
    user_transactions = [txn.to_dict() for txn in transactions if txn.sender_id == user_id or txn.receiver_id == user_id]

    return jsonify(user_transactions), 200
