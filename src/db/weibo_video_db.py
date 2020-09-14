#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @title: 
# @author: luowen<loovien@163.com>
# @website: https://loovien.github.com
# @time: 9/14/2020 10:35 PM

import hashlib
import logging

from src.util import pure_title, pure_url
from src.models.video import VideoItem
from src.db.sqlite import Sqlite3Record
from sqlite3 import Cursor

logger = logging.getLogger(__name__)


class WeiBoVideoDB(Sqlite3Record):

    def exists(self, code: str) -> bool:
        cursor: Cursor = self.database.cursor()
        cursor.execute("select count(1) as cnt from videos where code = ?", (code,))
        result = cursor.fetchone()
        cursor.close()
        if result[0] <= 0:
            return False
        return True

    def record_videos(self, data: VideoItem) -> bool:
        cursor: Cursor = self.database.cursor()
        code: str = hashlib.md5(pure_url(data.src).encode("utf-8")).hexdigest()
        if len(code.strip()) <= 0:
            logger.error("record row: {} not contain code field".format(data))
            raise ValueError("row must contain code field")
        if self.exists(code):
            logger.info("code:{} is record before".format(code))
            return False
        sql = "insert into videos (title, code, url, img, href) values (?, ?, ?, ?, ?)"
        img: str = code + ".jpg"
        cursor.execute(sql, (pure_title(data.title), code, pure_url(data.src), img, data.href))
        self.database.commit()
        cursor.close()
        affect_row = cursor.rowcount
        if affect_row <= 0:
            logger.error("sql: {} data: {} not success".format(sql, data))
            return False
        return True

    def current_videos_cursor(self):
        cursor: Cursor = self.database.cursor()
        cursor.execute("select max(id) from videos")
        result = cursor.fetchone()
        cursor.close()
        return result[0]

    def delta_videos(self, current_cursor: int):
        resp_data = []
        cursor: Cursor = self.database.cursor()
        cursor.execute("select id, title, url, href, code, created_date from videos where id > ?", (current_cursor,))
        result = cursor.fetchall()
        cursor.close()
        columns = ("id", "title", "url", "href", "code", "created_date",)
        for row in result:
            resp_data.append(dict(zip(columns, row)))
        return resp_data
