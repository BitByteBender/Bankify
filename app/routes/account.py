from flask import Blueprint, request, jsonify
from app.services.account_service import create_account

account = Blueprint('account', __name__)

@account.route('/create', methods=['POST'])
def create_user_account():
    data = request.json
    result = create_account(data)
    return jsonify(result), result.get('status', 400)

@account.route('/admin/deposit', methods=['POST'])
def admin_deposit():
    data = request.json
    result = admin_deposit_to_account(data)
    return jsonify(result), result.get('status', 400)

@account.route('/admin/withdraw', methods=['POST'])
def admin_withdraw():
    data = request.json
    result = admin_withdraw_from_account(data)
    return jsonify(result), result.get('status', 400)

@account.route('/transaction-count/<user_id>', methods=['GET'])
def get_transaction_count(user_id):
    result = get_transaction_count_by_user(user_id)
    return jsonify(result), 200

@account.route('/total-transactions', methods=['GET'])
def get_total_transactions():
    result = get_total_transaction_count()
    return jsonify(result), 200

@account.route('/balance/<account_id>', methods=['GET'])
def get_account_balance(account_id):
    result = get_account_balance(account_id)
    return jsonify(result), 200

@account.route('/balance/total', methods=['GET'])
def get_total_balance():
    result = get_total_balance()
    return jsonify(result), 200

@account.route('/users/<user_id>', methods=['GET'])
def get_single_user(user_id):
    result = find_user_by_id(user_id)
    return jsonify(result), 200

@account.route('/users', methods=['GET'])
def get_all_users():
    result = get_all_users()
    return jsonify(result), 200

@transaction.route('/details/<transaction_id>', methods=['GET'])
def get_sender_receiver_details(transaction_id):
    result = get_sender_receiver_details(transaction_id)
    return jsonify(result), 200
