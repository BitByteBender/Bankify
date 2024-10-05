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

    # trx = relationship("Transaction", backref="account_transactions",
    # cascade="all, delete-orphan", foreign_keys="Transaction.account_id")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<Account id={self.id}, user_id='{self.user_id}', balance={self.balance}>"

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than 0")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        self.save()

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than 0")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        self.save()

    def transfer(self, amount, to_account):
        if amount <= 0:
            raise ValueError("Transfer amount must be greater than 0")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        to_account.balance += amount
        self.save()
        to_account.save()

    def is_active(self):
        return not self.on_hold

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'balance': self.balance,
            'credits': self.credits,
            'on_hold': self.on_hold,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
