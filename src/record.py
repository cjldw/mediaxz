# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:
from __future__ import annotations
import logging

import shutil
import threading
import hashlib
from typing import Dict, Any
from json import load, dump, JSONDecodeError
from src.dl.download import Download
from queue import Queue
from src.config import setting_get
from typing import List
from src.models.video import Video
from src.db.sqlite import Sqlite3Record
from pathlib import Path
from src.util import pure_url
from datetime import datetime

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
    def acquire(options: Dict[str, Any]) -> Recoder:
        record_locker.acquire()
        if Recoder.__recorder is None:
            maxsize = setting_get("queue_size")
            queue: Queue = Queue(maxsize=maxsize if maxsize > 0 else 1000)
            Recoder.__recorder = Recoder()
            Recoder.queue_channel = queue
            Recoder.__recorder.options = options
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

    def dispatch_video(self, item: Video) -> None:
        video_hash: str = hashlib.md5(pure_url(item.src).encode("utf-8")).hexdigest()
        if Sqlite3Record.acquire(self.__recorder.options).exists(video_hash):
            logger.info("video_hash: {} item: {} is record in sqlite db".format(video_hash, item))
            return None
        logger.info("record dispatch data: {}".format(item))
        if not Sqlite3Record.acquire(self.__recorder.options).record_videos(item):
            logger.error("video: {} record to sqlite db failure".format(item))
            return None
        return self.__recorder.queue_channel.put(item)

    def load_dump(self) -> int:
        download_dir = Path(setting_get("download_output"))
        dumpfile = download_dir.joinpath("__index.json")
        if not download_dir.exists() or not dumpfile.exists():
            return 0
        with open(dumpfile, "r", encoding="utf-8") as fd:
            try:
                result: dict = load(fd)
                return result.get("cursor", 0)
            except JSONDecodeError as e:
                logger.error("json decode failure, err: {}".format(e.args))
            return 0

    def reset_dump(self, current_cursor: int) -> bool:
        download_dir = Path(setting_get("download_output"))
        if not download_dir.exists():
            download_dir.mkdir(mode=644, parents=True)
        dumpfile = download_dir.joinpath("__index.json")
        with open(dumpfile, mode="w", encoding="utf-8") as fd:
            dump({"cursor": current_cursor, "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, fd,
                 ensure_ascii=False)
        return True

    def export_json(self):
        download_dir = Path(setting_get("download_output"))
        if not download_dir.exists():
            download_dir.mkdir(mode=644, parents=True)
        abs_file = download_dir.joinpath("videos.json")
        if abs_file.exists():
            shutil.move(abs_file, download_dir.joinpath(
                "videos.json-{}".format(datetime.now().strftime("%Y%m%d%H%M%S"))))
        result = Sqlite3Record.acquire(self.__recorder.options).delta_videos(self.load_dump())
        with open(abs_file, mode="w", encoding="utf-8") as fd:
            dump(result, fd, indent="  ", ensure_ascii=False)
        logger.info("export all video to videos.json")
        self.reset_dump(Sqlite3Record.acquire(self.__recorder.options).current_videos_cursor())

    def dispose(self):
        self.queue_channel.join()
