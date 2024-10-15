from flask import Blueprint, request, jsonify
from models import storage
from models.account import Account
from models.transaction import Transaction

transactions_bp = Blueprint('transactions_bp', __name__)

@transactions_bp.route('/withdraw', methods=['POST'])
def withdraw():
    data = request.get_json()
    user_id = data.get('user_id')
    amount = data.get('amount')

    account = storage.get(Account, user_id)
    if account and account.balance >= amount:
        account.balance -= amount
        transaction = Transaction(user_id=user_id, amount=-amount)
        storage.new(transaction)
        storage.save()
        return jsonify({"message": "Withdrawal successful", "new_balance": account.balance}), 200
    else:
        return jsonify({"error": "Insufficient balance"}), 400

@transactions_bp.route('/deposit', methods=['POST'])
def deposit():
    data = request.get_json()
    user_id = data.get('user_id')
    amount = data.get('amount')

    account = storage.get(Account, user_id)
    if account:
        account.balance += amount
        transaction = Transaction(user_id=user_id, amount=amount)
        storage.new(transaction)
        storage.save()
        return jsonify({"message": "Deposit successful", "new_balance": account.balance}), 200
    else:
        return jsonify({"error": "Account not found"}), 400

