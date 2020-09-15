# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc: crawl

from src.website.weib import WeiB
from src.website.huaban import HuaBan


class CrawlFactory(object):
    def __init__(self, options: dict):
        self.options = options

    def crawl(self):
        clazz = self.options.get("website", None)
        if not clazz or len(clazz) <= 0:
            raise ValueError("clazz not configuration")
        if clazz == WeiB.name:
            return WeiB(self.options)
        if clazz == HuaBan.name:
            return HuaBan(self.options)
