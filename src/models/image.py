#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @title: 
# @author: luowen<loovien@163.com>
# @website: https://loovien.github.com
# @time: 9/14/2020 10:18 PM


class ImageItem(object):

    def __init__(self, url: str, width: int = 0, height: int = 0, hash_code: str = None, title: str = None):
        self.url = url
        self.width = width
        self.height = height
        self.hash = hash_code
        self.title = title

    def __str__(self) -> str:
        return "url: {}, width: {}, height:{} hash: {} title: {} ".format(self.url, self.width, self.height, self.hash,
                                                                          self.title)
