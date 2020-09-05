#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @title: 
# @author: luowen<loovien@163.com>
# @website: https://loovien.github.com
# @time: 9/5/2020 5:23 PM

import PyInstaller.__main__

if __name__ == '__main__':
    PyInstaller.__main__.run([
        "--name=mediaxz",
        "--onefile",
        "--clean",
        "--icon=favicon.ico",
        "main.py"
    ])
