# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:
from __future__ import annotations
import logging

import threading
from src.dl.download import Download
from queue import Queue
from src.config import setting_get
from typing import List
from src.models.video import Video

record_locker = threading.RLock()
logger = logging.getLogger(__name__)


class Recoder(object):
    __recorder = None

    queue_channel: Queue = None

    def __init__(self):
        record_locker.acquire()
        if self.__recorder is not None:
            record_locker.release()
            raise ValueError("record initialized")
        record_locker.release()

    @staticmethod
    def acquire() -> Recoder:
        record_locker.acquire()
        if Recoder.__recorder is None:
            maxsize = setting_get("queue_size")
            queue: Queue = Queue(maxsize=maxsize if maxsize > 0 else 1000)
            Recoder.__recorder = Recoder()
            Recoder.queue_channel = queue
            Recoder.__recorder.threads: List[Download] = []
            # initialize download thread
            thread_num = setting_get("download_thread_num")
            for index in range(0, thread_num):
                logger.info("start download thread: {}".format(index))
                thread: Download = Download(queue)
                Recoder.__recorder.threads.append(thread)
                thread.setName("download-thread-{}".format(index))
                thread.start()

        record_locker.release()
        return Recoder.__recorder

    def dispatch_video(self, item: Video):
        logger.info("record dispatch data: {}".format(item))
        return self.__recorder.queue_channel.put(item)

    def dispose(self):
        self.queue_channel.join()
