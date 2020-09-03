# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc: 日志管理


import logging
from logging import Formatter
from logging import StreamHandler
from logging.handlers import RotatingFileHandler


def config_logging():
    stream = StreamHandler()
    file = RotatingFileHandler(filename="app.log", encoding="utf-8", backupCount=10)

    output = Formatter("%(asctime)s:[%(levelname)s]:%(filename)s:%(lineno)d: %(message)s")

    stream.setFormatter(output)
    file.setFormatter(output)

    stream.setLevel(logging.INFO)
    file.setLevel(logging.INFO)
    logging.basicConfig(handlers=[stream, file], level=logging.INFO)
