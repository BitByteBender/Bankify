#!/usr/bin/env python3

from models.base_model import BaseModel

class Transaction(BaseModel):
    def __init__(self, user_id, amount):
        super().__init__()
        self.user_id = user_id
        self.amount = amount
        self.transaction_type = "deposit" if amount > 0 else "withdrawal"

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'amount': self.amount,
            'transaction_type': self.transaction_type
        }

