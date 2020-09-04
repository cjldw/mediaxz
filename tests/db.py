# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

import unittest

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
