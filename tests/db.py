# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

import unittest

from src.db.sqlite import Sqlite3Record
import sqlite3

from src.config import setting_get


class DbTest(unittest.TestCase):

    def test_db(self):
        a = Sqlite3Record.load().exists("luowen")
        print(a)
