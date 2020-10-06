# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

import unittest

from src.tools.title_builder import title_gen


class TitleTest(unittest.TestCase):

    def test_title(self):
        title = title_gen()
        print(title)
