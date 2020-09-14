# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

import unittest

import os
import json
from src.db.sqlite import Sqlite3Record
import sqlite3
import logging

from src.models.video import VideoItem

from src.logs import config_logging
from pathlib import Path
import pathlib

from src.config import setting_get
import time

logger = logging.getLogger(__name__)


class DbTest(unittest.TestCase):

    def test_record_videos(self):
        video = VideoItem(title="luowen", img_src="https://img2.zhanqi.com/aa.jgp", src="xxxxxxxxxxxxx")
        a = Sqlite3Record.acquire().record_videos(video)
        print(a)

    def test_max_cursor_videos(self):
        cursor = Sqlite3Record.acquire().current_videos_cursor()
        print(cursor)

    def test_videos(self):
        result = Sqlite3Record.acquire().delta_videos(0)
        print(result)

    def test_export(self):
        return
        config_logging()
        video = VideoItem(title="罗文辉就是我", img_src="https://img2.zhanqi.com/aa.jgp", src="xxxxxxxxxxxxx")
        with open("d.json", mode="w", encoding="utf-8") as fd:
            json.dump({"title": video.title, "img": video.img_src, "src": video.src}, fd, indent="  ",
                      ensure_ascii=False)

        logger.info("hehel uowen {name} {fmt}".format(name="luowen", fmt="{}"))

        print("end")
        os.path("./")
