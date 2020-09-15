# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

import urllib
from pathlib import Path

from urllib.parse import urlparse, ParseResult
import shutil

from datetime import datetime

a = {
    "luowen": "haha",
}


def main():
    url = "//hbimg.huabanimg.com/5405ea81d6912d96adbf866438317c8f1a27cf844b38c-i64GS2_fw236/format/webp?r=23&a=111"
    result: ParseResult = urlparse(url)
    print(result)


class D(object):
    name = None

    def __init__(self):
        self.name = "luowen"

    class DD(object):
        def getname(self):
            pass

    def OK(self):
        sub = self.DD()
        sub.getname()


if __name__ == '__main__':
    d = D()
    print(d.name)
    d.OK()
