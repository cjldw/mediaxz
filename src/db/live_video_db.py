# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

import logging
from src.db.sqlite import Sqlite3Record
from src.models.live_video import LiveVideo

logger = logging.getLogger(__name__)


class LiveStreamDb(Sqlite3Record):

    def record_video(self, data: LiveVideo) -> int:
        cursor = self.database.cursor()
        sql = "insert into videos_stream (title, url, code, created_date) values (?, ?, ?, ?)"
        cursor.execute(sql, (data.title, data.url, data.code, data.created_date), )
        self.database.commit()
        rowcount = cursor.rowcount
        cursor.close()
        return rowcount

    def record_exists(self, code: str) -> bool:
        cursor = self.database.cursor()
        sql = "select count(1) as cnt from videos_stream where code = ? limit 1"
        cursor.execute(sql, (code,), )
        result = cursor.fetchone()
        return result[0] > 0

    def record_index(self, index: int):
        cursor = self.database.cursor()
        sql = "insert into videos_stream_index (record_index) values (?)"
        cursor.execute(sql, (index,), )
        self.database.commit()
        result = cursor.rowcount
        cursor.close()
        return result

    def last_playing(self) -> int:
        cursor = self.database.cursor()
        sql = "select record_index from videos_stream_index order by id desc limit 1"
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result[0]

    def video_url(self, index: int) -> str:
        cursor = self.database.cursor()
        sql = "select url from videos_stream where id >= ? limit 1"
        cursor.execute(sql, (index,), )
        result = cursor.fetchone()
        cursor.close()
        return result[0]
