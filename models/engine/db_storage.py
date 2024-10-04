#!/usr/bin/env python3

import models
import sqlalchemy
from models.base_model import BaseModel, Base
from models.users import User
from models.accounts import Account
from models.trx import Transaction
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError


classes = {"User": User, "Account": Account, "Transaction": Transaction}

class DBStorage:
    """ Interacts with the MySQL database """
    __engine = None
    __session = None

    def __init__(self):
        """ Instantiate a DBStorage obj """
        BK_MYSQL_USR = getenv('BK_MYSQL_USR')
        BK_MYSQL_PWD = getenv('BK_MYSQL_PWD')
        BK_MYSQL_HOST = getenv('BK_MYSQL_HOST')
        BK_MYSQL_PORT = getenv('BK_MYSQL_PORT')
        BK_MYSQL_DB = getenv('BK_MYSQL_DB')
        Bk_ENV = getenv('BK_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:{}/{}'.
                                       format(Bk_MYSQL_USR,
                                              BK_MYSQL_PWD,
                                              BK_MYSQL_HOST,
                                              BK_MYSQL_PORT,
                                              BK_MYSQL_DB))

        if BK_ENV == "drop":
            Base.metadata.drop_all(self.__engine)

    def new(self, obj):
        """ Add the object to the current db session """
        self.__session.add(obj)

    def save(self):
        """ Commits all changes of the current database session """
        try:
            self.__session.commit()
        except SQLAlchemyError as e:
            self.rollback()
            raise

    def delete(self, obj=None):
        """ Delete obj from the current database session """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """ Creates all tables in the database and create the session """
        Base.metadata.create_all(self.__engine)
        self.__session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(self.__session_factory)

    def all(self, cls=None):
        """ Query on the current database session """
        result = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    result[key] = obj
        return result

    def get(self, cls, id):
        """ Retrieves a single obj """
        if isinstance(cls, str):
            cls = classes.get(cls)
        if cls not in classes.values():
            return None

        return self.__session.query(cls).get(id)

    def count(self, cls=None):
        """ Counts the number of objects in storage """
        all_class = classes.values()
        if not cls:
            count = 0
            for c in all_class:
                count += len(models.storage.all(c).values())
        else:
            count = len(models.storage.all(cls).values())

        return count

    def rollback(self):
        """ Rollback the current session """
        if self.__session:
            self.__session.rollback()

    def close(self):
        """ Remove the current session """
        if self.__session:
            self.__session.close()
