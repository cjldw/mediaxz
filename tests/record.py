# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

import unittest

import shutil

from pathlib import Path
from src.util import remove_emoji

from .URL import a


class TestRecord(unittest.TestCase):

    def test_export_json(self):
        a.update({"age": 32})
        self.test_xx()

    def test_xx(self):
        src = Path("tests/test.mp4")

        # Path(src.parent).joinpath("tmp").mkdir(mode=664)
        shutil.move(src, Path(src.parent).joinpath("tmp", src.name))
