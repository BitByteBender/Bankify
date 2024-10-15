#!/usr/bin/env python3

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, DECIMAL, Integer, Boolean
from sqlalchemy.orm import relationship

class Account(BaseModel, Base):
    __tablename__ = "accounts"

    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    balance = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    credits = Column(Integer, nullable=False, default=0)
    on_hold = Column(Boolean, default=False)

    # trx = relationship("Transaction", backref="account_transactions", cascade="all, delete-orphan", foreign_keys="Transaction.account_id")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return "<Account id={}, user_id='{}', balance={}>".format(self.id, self.user_id, self.balance)

    def __init__(self, user_id, initial_balance=0.0):
        super().__init__()
        self.user_id = user_id
        self.balance = initial_balance

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'balance': self.balance
        }
