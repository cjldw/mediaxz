# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

import urllib
from pathlib import Path

from urllib.parse import urlparse, ParseResult
import shutil

import time
import requests
from datetime import datetime

a = {
    "luowen": "haha",
}


def main():
    url = "//hbimg.huabanimg.com/5405ea81d6912d96adbf866438317c8f1a27cf844b38c-i64GS2_fw236/format/webp.gif?r=23&a=111"
    result: ParseResult = urlparse(url)
    print(result)


def download():
    url = "http://wx4.sinaimg.cn/large/79a00895ly1gfsxked5l0g205k07tqv5.gif?"
    parse_result: ParseResult = urlparse(url)
    download_url: str = "{}://{}{}?{}".format(parse_result.scheme if len(parse_result) > 0 else "https",
                                              parse_result.netloc, parse_result.path, parse_result.query)
    download_img_resp = requests.get(download_url, stream=True)
    if download_img_resp.status_code != 200:
        print("item: {} images download failure, result: {}", download_url, download_img_resp.text)
        time.sleep(0.3)
    try:
        abs_file = Path(".").joinpath(Path(parse_result.path).name)
        with open(abs_file, "wb") as out_file:
            shutil.copyfileobj(download_img_resp.raw, out_file)
        del download_img_resp
        # self.record_queue.put(item)
    except Exception as e:
        print("failure error: {}".format(e))


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
    # main()
    download()
