#!/usr/bin/python3

from os import getenv


storage_t = getenv("BK_TYPE_STORAGE")

if storage_t == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
storage.reload()
