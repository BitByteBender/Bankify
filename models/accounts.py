#!/usr/bin/env python3

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, DECIMAL, Integer, Boolean

class Account(BaseModel, Base):
    __tablename__ = "accounts"

    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    balance = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    credits = Column(Integer, nullable=False, default=0)
    on_hold = Column(Boolean, default=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return "<Account id={}, user_id='{}', balance={}>".format(self.id, self.user_id, self.balance)
