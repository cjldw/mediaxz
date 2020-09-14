#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @title: 
# @author: luowen<loovien@163.com>
# @website: https://loovien.github.com
# @time: 9/5/2020 12:30 AM


class VideoItem(object):
    def __init__(self, title: str, img_src: str, src: str, href: str):
        self.title = title
        self.img_src = img_src
        self.src = src
        self.href = href
