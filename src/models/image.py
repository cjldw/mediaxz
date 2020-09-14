#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @title: 
# @author: luowen<loovien@163.com>
# @website: https://loovien.github.com
# @time: 9/14/2020 10:18 PM


class ImageItem(object):

    def __init__(self, url: str, width: int, height: int, hash: str = None):
        self.url = url
        self.width = width
        self.height = height
        self.hash = hash

    def __str__(self) -> str:
        return "url: {}, width: {}, height:{} hash: ".format(self.url, self.width, self.height, self.hash)
