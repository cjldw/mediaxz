#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @title: 
# @author: luowen<loovien@163.com>
# @website: https://loovien.github.com
# @time: 9/15/2020 12:11 AM

import unittest
from src.models.image import ImageItem
from src.db.huaban_image_db import HuaBanDb


class TestHuaBanDb(unittest.TestCase):

    def setUp(self) -> None:
        self.db = HuaBanDb({"db": "E:\codelab\python\mediaxz\dist\huaban.db"})

    def test_record(self):
        url = "//hbimg.huabanimg.com/5405ea81d6912d96adbf866438317c8f1a27cf844b38c-i64GS2_fw236/format/webp"
        data = ImageItem(url=url, width=200, height=400, hash="luwoen")
        self.db.record(data)

    def test_exists(self):
        ok = self.db.exists("luowen")
        print(ok)
