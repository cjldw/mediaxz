# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

import unittest

from src.util import remove_emoji

from .URL import a
from .image import xx


class TestRecord(unittest.TestCase):

    def test_export_json(self):
        a.update({"age": 32})
        self.test_xx()

    def test_xx(self):
        xx()
