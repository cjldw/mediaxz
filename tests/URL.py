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


def main():
    print("luowen        ".strip())
    a = [(1, 2, 3, 4)]
    b = [("name", "age", "hobby", "lover")]

    print(datetime.now().strftime("%Y-%m-%d %H:%t:%S"))
    print(a * 3)
    print(dict(zip(b * 3, a * 3)))


if __name__ == '__main__':
    main()
