#!/usr/bin/env python3

from models.accounts import Account
from models.transaction import Transaction
from models import storage

def process_withdrawal(user_id, amount):
    account = storage.get(Account, user_id)
    if account and account.balance >= amount:
        account.balance -= amount
        transaction = Transaction(user_id=user_id, amount=-amount)
        storage.new(transaction)
        storage.save()
        return {"status": "success", "new_balance": account.balance}
    return {"status": "failed", "error": "Insufficient balance or account not found"}

def process_deposit(user_id, amount):
    account = storage.get(Account, user_id)
    if account:
        account.balance += amount
        transaction = Transaction(user_id=user_id, amount=amount)
        storage.new(transaction)
        storage.save()
        return {"status": "success", "new_balance": account.balance}
    return {"status": "failed", "error": "Account not found"}

