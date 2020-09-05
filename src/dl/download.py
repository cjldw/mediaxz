#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @title: 
# @author: luowen<loovien@163.com>
# @website: https://loovien.github.com
# @time: 9/5/2020 12:27 AM

from __future__ import annotations

import logging
import hashlib
import requests
import shutil

from pathlib import Path
from threading import Thread
from src.models.video import Video
from src.db.sqlite import Sqlite3Record
from queue import Queue
from src.config import setting_get

logger = logging.getLogger(__name__)


class Download(Thread):
    daemon = True

    def __init__(self, queue: Queue):
        super().__init__()
        self.queue: Queue = queue
        self.download_dir = setting_get("download_output")

    def run(self) -> None:
        while True:
            video: Video = self.queue.get()
            logger.info("{} handler {}".format(self.getName(), video.title))
            try:
                self.download_img(video)
                download_success = self.download_video(video)
                logger.info("download video: {} status: {}".format(video.title, download_success))
            except Exception as e:
                logger.error("download video failre, err:{}".format(e.args))
            finally:
                self.queue.task_done()

    def download_img(self, video: Video) -> bool:
        download_img_resp = requests.get(video.img_src, stream=True)
        if download_img_resp.status_code != 200:
            logger.error("item: {} images download failure, result: {}", video, download_img_resp.text)
            return False
        filename: str = hashlib.md5(video.img_src.encode("utf-8")).hexdigest() + ".jpg"
        download_dir = Path(self.download_dir)
        if not download_dir.exists():
            download_dir.mkdir(mode=644, parents=True)
        abs_file = download_dir.joinpath(filename)
        logger.info("download image file: {}".format(abs_file))
        with open(abs_file, "wb") as out_file:
            shutil.copyfileobj(download_img_resp.raw, out_file)
        del download_img_resp
        return True

    def download_video(self, video: Video) -> bool:
        download_video_resp = requests.get(video.src, stream=True)
        if download_video_resp.status_code != 200:
            logger.error("download video: {} failre, err: {}".format(video.src, download_video_resp.text))
            self.queue.task_done()
            return False

        filename: str = hashlib.md5(video.src.encode("utf-8")).hexdigest() + ".mp4"
        abs_file = Path(self.download_dir).joinpath(filename)
        logger.info("download video file: {}".format(abs_file))
        with open(abs_file, "wb") as out_file:
            shutil.copyfileobj(download_video_resp.raw, out_file)
        del download_video_resp

        return True
