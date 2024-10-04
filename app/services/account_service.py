from flask import jsonify
from app import db
from app.models import Account, Transaction

class AccountService:

    @staticmethod
    def create_account(user_id, initial_deposit):
        """Creates a new bank account for a user with an initial deposit."""
        if initial_deposit <= 0:
            return jsonify({"error": "Initial deposit must be greater than zero."}), 400

        new_account = Account(user_id=user_id, balance=initial_deposit)
        db.session.add(new_account)
        db.session.commit()
        return jsonify({"message": "Account created successfully.", "account_id": new_account.id}), 201

    @staticmethod
    def get_account_balance(account_id):
        """Retrieves the balance of the specified account."""
        account = Account.query.get(account_id)
        if account is None:
            return jsonify({"error": "Account not found."}), 404
        return jsonify({"account_id": account.id, "balance": account.balance}), 200

    @staticmethod
    def deposit(account_id, amount):
        """Deposits an amount into the specified account."""
        if amount <= 0:
            return jsonify({"error": "Deposit amount must be greater than zero."}), 400

        account = Account.query.get(account_id)
        if account is None:
            return jsonify({"error": "Account not found."}), 404

        account.balance += amount
        new_transaction = Transaction(account_id=account.id, amount=amount, transaction_type='deposit')
        db.session.add(new_transaction)
        db.session.commit()

        return jsonify({"message": "Deposit successful.", "new_balance": account.balance}), 200

    @staticmethod
    def withdraw(account_id, amount):
        """Withdraws an amount from the specified account."""
        if amount <= 0:
            return jsonify({"error": "Withdrawal amount must be greater than zero."}), 400

        account = Account.query.get(account_id)
        if account is None:
            return jsonify({"error": "Account not found."}), 404

        if account.balance < amount:
            return jsonify({"error": "Insufficient funds."}), 400

        account.balance -= amount
        new_transaction = Transaction(account_id=account.id, amount=-amount, transaction_type='withdrawal')
        db.session.add(new_transaction)
        db.session.commit()

        return jsonify({"message": "Withdrawal successful.", "new_balance": account.balance}), 200

    @staticmethod
    def get_account_statement(account_id):
        """Retrieves the transaction history for the specified account."""
        account = Account.query.get(account_id)
        if account is None:
            return jsonify({"error": "Account not found."}), 404

        transactions = Transaction.query.filter_by(account_id=account.id).all()
        transaction_list = [{"transaction_id": t.id, "amount": t.amount, "type": t.transaction_type} for t in transactions]

        return jsonify({"account_id": account.id, "transactions": transaction_list}), 200