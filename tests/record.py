# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

import unittest


from src.util import remove_emoji


class TestRecord(unittest.TestCase):

    def test_export_json(self):
        txt = "瞄瞄， 伙就是😆"
        print(txt)
        print(remove_emoji(txt))
