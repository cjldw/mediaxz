# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:
from __future__ import annotations

import threading
from queue import Queue

record_locker = threading.Lock()


class Recoder(object):
    __recorder = None

    queue_channel: Queue = None

    def __init__(self):
        record_locker.acquire()
        if self.__recorder is not None:
            record_locker.release()
            raise ValueError("record initialized")
        self.__recorder = self
        record_locker.release()

    @staticmethod
    def load(self) -> Recoder:
        record_locker.acquire()
        if self.__recorder is None:
            self.__recorder = Recoder()
            self.__recorder.queue_channel = Queue(maxsize=10000)
        record_locker.release()
        return self.__recorder

    def dispatch(self, item: dict):
        return self.__recorder.queue_channel.put_nowait(item)
