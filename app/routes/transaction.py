from flask import Blueprint, request, jsonify
from app.services.account_service import peer_to_peer_transaction

transaction = Blueprint('transaction', __name__)

@transaction.route('/transfer', methods=['POST'])
def transfer_funds():
    data = request.json
    result = peer_to_peer_transaction(data)
    return jsonify(result), result.get('status', 400)