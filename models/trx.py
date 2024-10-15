#!/usr/bin/env python3

import enum
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, DECIMAL, String, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime


class TransactionStatus(enum.Enum):
    SENT = "Sent"
    RECEIVED = "Received"
    DEPOSITED = "Deposit"
    WITHDRAWN = "Withdraw"


class Transaction(BaseModel, Base):
    __tablename__ = "transactions"

    sender_id = Column(String(60), ForeignKey('accounts.id'), nullable=False)
    receiver_id = Column(String(60), ForeignKey('accounts.id'), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    transaction_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    status = Column(Enum(TransactionStatus), nullable=False)
    sender = relationship("Account", foreign_keys=[sender_id], backref="sent_transactions")
    receiver = relationship("Account", foreign_keys=[receiver_id], backref="received_transactions")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return "<Transaction id={}, sender_id='{}', receiver_id='{}', amount={}, status={}>".format(self.id, self.sender_id, self.receiver_id, self.amount, self.status)

    def to_dict(self):
        """ Instance convertion to a dictionary format """
        new_dict = super().to_dict()
        new_dict['status'] = self.status.value
        return new_dict
