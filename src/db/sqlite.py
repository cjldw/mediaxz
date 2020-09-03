# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

from __future__ import annotations
import sqlite3
import threading

from sqlite3.dbapi2 import Cursor
from sqlite3 import dbapi2
from src.config import setting_get

sqlite_locker = threading.Lock()


class Sqlite3Record(object):
    __db: dbapi2 = None
    __instance: Sqlite3Record = None

    def __init__(self):
        sqlite_locker.acquire()
        if self.__instance is not None:
            sqlite_locker.release()
            raise ValueError("__db initialized")
        self.__instance = self
        sqlite_locker.release()

    @staticmethod
    def load(db: str = None):
        sqlite_locker.acquire()
        if Sqlite3Record.__instance is not None:
            sqlite_locker.release()
            return Sqlite3Record.__instance
        Sqlite3Record.__instance = Sqlite3Record()
        if db is None:
            db = setting_get("db")
        Sqlite3Record.__instance.__db = sqlite3.connect(database=db)
        sqlite_locker.release()
        return sql

    def exists(self, code: str) -> bool:
        cursor: Cursor = self.__db.cursor()
        cursor.execute("select count(1) as cnt from videos where code = ?", (code,))
        result = cursor.fetchone()
        print(result)
        cursor.close()
