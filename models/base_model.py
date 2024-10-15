#!/usr/bin/env python3

from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base
import models
import uuid


Base = declarative_base()


class BaseModel:
    __abstract__ = True
    id = Column(String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', str(uuid.uuid4()))
        self.created_at = kwargs.get('created_at', datetime.utcnow())
        self.updated_at = kwargs.get('updated_at', datetime.utcnow())
        for k, val in kwargs.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(self, k, val)

    def save(self):
        """ Updates the 'updated_at' and saves the model """
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """ Convert the instance to a dictionary format """
        new_dict = {}
        for col in self.__table__.columns:
            value = getattr(self, col.name)
            if isinstance(value, datetime):
                value = value.isoformat()
            elif isinstance(value, Decimal):
                value = float(value)
            new_dict[col.name] = value
        return new_dict

    def delete(self):
        """ Delete the current instance from the storage """
        models.storage.delete(self)
