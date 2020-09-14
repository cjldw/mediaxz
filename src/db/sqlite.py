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
from src.util import pure_url, pure_title

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
        code: str = hashlib.md5(pure_url(data.src).encode("utf-8")).hexdigest()
        if len(code.strip()) <= 0:
            sqlite_locker.release()
            logger.error("record row: {} not contain code field".format(data))
            raise ValueError("row must contain code field")
        if self.exists(code):
            sqlite_locker.release()
            logger.info("code:{} is record before".format(code))
            return False
        sql = "insert into videos (title, code, url, img, href) values (?, ?, ?, ?, ?)"
        img: str = code + ".jpg"
        cursor.execute(sql, (pure_title(data.title), code, pure_url(data.src), img, data.href))
        self.__db.commit()
        affect_row = cursor.rowcount
        sqlite_locker.release()
        if affect_row <= 0:
            logger.error("sql: {} data: {} not success".format(sql, data))
            return False
        return True

    def current_videos_cursor(self):
        cursor: Cursor = self.__db.cursor()
        cursor.execute("select max(id) from videos")
        result = cursor.fetchone()
        cursor.close()
        return result[0]

    def delta_videos(self, current_cursor: int):
        resp_data = []
        cursor: Cursor = self.__db.cursor()
        cursor.execute("select id, title, url, href, code, created_date from videos where id > ?", (current_cursor,))
        result = cursor.fetchall()
        cursor.close()
        columns = ("id", "title", "url", "href", "code", "created_date",)
        for row in result:
            resp_data.append(dict(zip(columns, row)))
        return resp_data
