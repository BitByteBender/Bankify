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
