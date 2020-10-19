#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @title: 
# @author: luowen<loovien@163.com>
# @website: https://loovien.github.com
# @time: 9/14/2020 11:49 PM

import time
import logging
from typing import List
from sqlite3 import Cursor
from src.models.image import ImageItem
from src.db.sqlite import Sqlite3Record

logger = logging.getLogger(__name__)


class GaoXiaoGifDb(Sqlite3Record):

    def record(self, image: ImageItem) -> None:
        cursor: Cursor = self.database.cursor()
        sql = "insert into images (url, title, width, height, hash, created_date) values (?, ?, ?, ?, ?, ?)"
        now_time = time.strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(sql, (image.url, image.title, image.width, image.height, image.hash, now_time,))
        logger.info("sql: {}, bind: {}".format(sql, str(image)))
        self.database.commit()
        cursor.close()

    def exists(self, url: str) -> bool:
        cursor: Cursor = self.database.cursor()
        cursor.execute("select count(1) as cnt from images where url = ?", (url,))
        result = cursor.fetchone()
        cursor.close()
        return result[0] > 0

    def max_id(self) -> int:
        cursor: Cursor = self.database.cursor()
        cursor.execute("select max(id) from images")
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result is not None else 0

    def rows(self, max_id: int) -> List[dict]:
        cursor: Cursor = self.database.cursor()
        cursor.execute("select id, url, hash, created_date from images where id >= ?", (max_id,))
        result = cursor.fetchall()
        cursor.close()
        columns = ("id", "url", "hash", "created_date",)
        resp_data = []
        for row in result:
            resp_data.append(dict(zip(columns, row)))
        return resp_data

    def record_max_id(self, image_id: int) -> bool:
        cursor: Cursor = self.database.cursor()
        cursor.execute("insert into image_record_index (record_index, created_date) values (?, ?)",
                       (image_id, time.strftime("%Y-%m-%d %H:%M:%S"),))
        self.database.commit()
        affected_row = cursor.rowcount
        cursor.close()
        return affected_row > 0

    def truncate_index(self) -> bool:
        cursor: Cursor = self.database.cursor()
        cursor.execute("delete from image_record_index")
        self.database.commit()
        affected_row = cursor.rowcount
        cursor.close()
        return affected_row > 0

    def current_index(self) -> int:
        cursor: Cursor = self.database.cursor()
        cursor.execute("select max(record_index) from image_record_index limit 1")
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result is not None else 0
