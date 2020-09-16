#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @title: 
# @author: luowen<loovien@163.com>
# @website: https://loovien.github.com
# @time: 9/14/2020 11:49 PM

import time
import logging
from sqlite3 import Cursor
from src.models.image import ImageItem
from src.db.sqlite import Sqlite3Record

logger = logging.getLogger(__name__)


class HuaBanDb(Sqlite3Record):

    def record(self, image: ImageItem) -> None:
        cursor: Cursor = self.database.cursor()
        sql = "insert into images (url, width, height, hash, created_date) values (?, ?, ?, ?, ?)"
        cursor.execute(sql, (image.url, image.width, image.height, image.hash, time.strftime("%Y-%m-%d %H:%M:%S"),))
        logger.info("sql: {}, bind: {}".format(sql, str(image)))
        self.database.commit()
        cursor.close()

    def exists(self, hash: str) -> bool:
        cursor: Cursor = self.database.cursor()
        cursor.execute("select count(1) as cnt from images where hash = ?", (hash,))
        result = cursor.fetchone()
        cursor.close()
        return result[0] > 0

    def max_id(self) -> int:
        cursor: Cursor = self.database.cursor()
        cursor.execute("select max(id) from images")
        result = cursor.fetchone()
        cursor.close()
        return result[0]

    def record_max_id(self, image_id: int) -> bool:
        cursor: Cursor = self.database.cursor()
        cursor.execute("insert into image_record_index (last_index, created_date) values (?, ?)",
                       (image_id, time.strftime("%Y-%m-%d %H:%M:%S"),))
        self.database.commit()
        affected_row = cursor.rowcount
        cursor.close()
        return affected_row > 0
