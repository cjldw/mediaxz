# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

from src.tools.notify import Reporting
import unittest


class Email(unittest.TestCase):

    def test_email(self):
        reporting = Reporting()
        reporting.sender("luowen", "ceshi")
