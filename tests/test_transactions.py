import unittest
from models.account import Account
from models.transaction import Transaction
from models import storage
from controllers.transactions_controller import process_withdrawal, process_deposit

class TestTransactions(unittest.TestCase):

    def setUp(self):
        self.user_id = "test_user"
        self.account = Account(user_id=self.user_id, initial_balance=100.0)
        storage.new(self.account)

    def test_withdrawal(self):
        result = process_withdrawal(self.user_id, 50.0)
        self.assertEqual(result['status'], 'success')
        self.assertEqual(self.account.balance, 50.0)

    def test_deposit(self):
        result = process_deposit(self.user_id, 50.0)
        self.assertEqual(result['status'], 'success')
        self.assertEqual(self.account.balance, 150.0)

    def tearDown(self):
        storage.delete(self.account)

if __name__ == '__main__':
    unittest.main()

