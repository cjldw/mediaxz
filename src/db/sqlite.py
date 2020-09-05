# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

from __future__ import annotations
import sqlite3
import threading
import logging
import hashlib
from sqlite3.dbapi2 import Cursor
from sqlite3 import dbapi2
from src.config import setting_get
from src.models.video import Video

sqlite_locker = threading.RLock()
logger = logging.getLogger(__name__)


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
    def acquire(db: str = None) -> Sqlite3Record:
        sqlite_locker.acquire()
        if Sqlite3Record.__instance is not None:
            sqlite_locker.release()
            return Sqlite3Record.__instance
        Sqlite3Record.__instance = Sqlite3Record()
        if db is None:
            db = setting_get("db")
        Sqlite3Record.__instance.__db = sqlite3.connect(database=db, timeout=3)
        sqlite_locker.release()
        return Sqlite3Record.__instance

    def exists(self, code: str) -> bool:
        sqlite_locker.acquire()
        cursor: Cursor = self.__db.cursor()
        cursor.execute("select count(1) as cnt from videos where code = ?", (code,))
        result = cursor.fetchone()
        cursor.close()
        sqlite_locker.release()
        if result[0] <= 0:
            return False
        return True

    def record_videos(self, data: Video) -> bool:
        sqlite_locker.acquire()
        cursor: Cursor = self.__db.cursor()
        code: str = hashlib.md5(data.src.encode("utf-8")).hexdigest()
        if len(code.strip()) <= 0:
            sqlite_locker.release()
            logger.error("record row: {} not contain code field".format(data))
            raise ValueError("row must contain code field")
        if self.exists(code):
            sqlite_locker.release()
            logger.info("code:{} is record before".format(code))
            return False
        sql = "insert into videos (title, code, url, img) values (?, ?, ?, ?)"
        img: str = hashlib.md5(data.img_src.encode("utf-8")).hexdigest() + ".jpg"
        cursor.execute(sql, (data.title, code, data.src, img))
        self.__db.commit()
        affect_row = cursor.rowcount
        sqlite_locker.release()
        if affect_row <= 0:
            logger.error("sql: {} data: {} not success".format(sql, data))
            return False
        return True
