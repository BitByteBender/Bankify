#!/usr/bin/env python3

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

class User(BaseModel, Base):
    __tablename__ = "users"

    full_name = Column(String(128), nullable=False)
    phone = Column(String(20), nullable=False, unique=True)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    account_activation_status = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    accounts = relationship("Account", backref="user", cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return "<User id={}, full_name='{}', email='{}', is_admin={}>".format(self.id, self.full_name, self.email, self.is_admin)
