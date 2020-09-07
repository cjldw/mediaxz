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

from src.models.video import Video

from pathlib import Path
import pathlib

from src.config import setting_get


class DbTest(unittest.TestCase):

    def test_db(self):
        video = Video(title="luowen", img_src="https://img2.zhanqi.com/aa.jgp", src="xxxxxxxxxxxxx")
        a = Sqlite3Record.acquire().record_videos(video)
        print(a)

        p = Path("luowen.txt")

    def test_export(self):
        video = Video(title="罗文辉就是我", img_src="https://img2.zhanqi.com/aa.jgp", src="xxxxxxxxxxxxx")
        with open("d.json", mode="w", encoding="utf-8") as fd:
            json.dump({"title": video.title, "img": video.img_src, "src": video.src}, fd, indent="  ", ensure_ascii=False)

        print("end")
        os.path("./")
