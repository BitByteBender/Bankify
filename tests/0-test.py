#!/usr/bin/env python3

from models import storage
from models.users import User
from models.accounts import Account
from models.trx import Transaction

def create_test_data():
    """ Function to create test data and save it to the database """

    # Create Users
    user1 = User(
        full_name="Alice Johnson",
        phone="1234567890",
        email="alice@example.com",
        password="alicepassword",
        address="123 Alice St.",
        account_activation_status=True
    )
    user2 = User(
        full_name="Bob Smith",
        phone="0987654321",
        email="bob@example.com",
        password="bobpassword",
        address="456 Bob Ave.",
        account_activation_status=True
    )

    # Save users to the database
    storage.new(user1)
    storage.new(user2)
    storage.save()

    print(f"Created Users: {user1.id}, {user2.id}")

    # Create Accounts for each User
    account1 = Account(user_id=user1.id, balance=1000.00)
    account2 = Account(user_id=user2.id, balance=1500.00)

    # Save accounts to the database
    storage.new(account1)
    storage.new(account2)
    storage.save()

    print(f"Created Accounts: {account1.id}, {account2.id}")

    # Create a Transaction from account1 to account2
    trx1 = Transaction(
        sender_id=account1.id,
        receiver_id=account2.id,
        amount=200.00
    )

    # Save transaction to the database
    storage.new(trx1)
    storage.save()

    print(f"Created Transaction: {trx1.id} from {trx1.sender_id} to {trx1.receiver_id}")

def retrieve_data():
    """ Retrieve and display test data from the database """
    # Fetch all users
    users = storage.all(User)
    print("\nUsers:")
    for user in users.values():
        print(user)

    # Fetch all accounts
    accounts = storage.all(Account)
    print("\nAccounts:")
    for account in accounts.values():
        print(account)

    # Fetch all transactions
    transactions = storage.all(Transaction)
    print("\nTransactions:")
    for trx in transactions.values():
        print(trx)

if __name__ == "__main__":
    # Create test data and insert into the database
    create_test_data()

    # Retrieve and display the data
    retrieve_data()
