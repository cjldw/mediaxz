# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

from __future__ import annotations
import sqlite3
import logging
from sqlite3 import dbapi2

logger = logging.getLogger(__name__)


class Sqlite3Record(object):
    database: dbapi2 = None

    def __init__(self, options: dict):
        dbname = options.get("website", "")
        if len(dbname) > 0:
            db = "{}.db".format(dbname)
            self.database = sqlite3.connect(database=db, timeout=3)
            return
        dbname = options.get("db", "")
        if len(dbname) <= 0:
            raise ValueError("db configuration not setting")
        self.database = sqlite3.connect(database=dbname, timeout=3)
