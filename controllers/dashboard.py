from flask import Blueprint, jsonify, request
from models.engine.db_storage import DBStorage
from models.accounts import Account
from models.trx import Transaction

dashboard_handler = Blueprint('dashboard_handler', __name__)

@dashboard_handler.route('/dashboard', methods=['GET'])
def get_dashboard_data():
    """ Retrieve dashboard data for the user """
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    accounts = DBStorage.all(Account)
    transactions = DBStorage.all(Transaction)

    user_accounts = [account.to_dict() for account in accounts.values() if account.user_id == user_id]
    user_transactions = [txn.to_dict() for txn in transactions.values() if txn.sender_id == user_id or txn.receiver_id == user_id]

    dashboard_data = {
        "accounts": user_accounts,
        "transactions": user_transactions,
    }

    return jsonify(dashboard_data), 200

@dashboard_handler.route('/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """ Retrieve statistics for the user """
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    accounts = DBStorage.all(Account)
    transactions = DBStorage.all(Transaction)

    user_accounts = [account for account in accounts.values() if account.user_id == user_id]
    user_transactions = [txn for txn in transactions.values() if txn.sender_id == user_id or txn.receiver_id == user_id]

    total_balance = sum(account.balance for account in user_accounts)
    total_deposits = sum(txn.amount for txn in user_transactions if txn.amount > 0)

    stats = {
        "total_balance": total_balance,
        "total_deposits": total_deposits,
        "transaction_count": len(user_transactions),
    }

    return jsonify(stats), 200
