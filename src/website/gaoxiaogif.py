# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

from abc import ABC
from queue import Queue
from threading import Thread
from pathlib import Path
from src.website.browser import Browser
from src.db.gaoxiaogif_db import GaoXiaoGifDb
from src.tools.videos import videos_export_json

from typing import List
from src.models.image import ImageItem
from urllib.parse import urlparse, ParseResult
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import os
import requests
import logging
import shutil
import time

logger = logging.getLogger(__name__)


class GaoXiaoGif(Browser, ABC):
    name = "gaoxiaogif"

    url = "http://www.gaoxiaogif.com/"

    # class Downloader():

    class Downloader(Thread):
        daemon = True

        def __init__(self, download_queue: Queue, output: str, **kwargs):
            if len(output) <= 0:
                raise ValueError("download output directory not setting")
            self.download_queue = download_queue
            # self.record_queue = record_queue
            self.output = Path(output)
            if not self.output.exists():
                self.output.mkdir(644, parents=True)
            super().__init__(**kwargs)

        def run(self) -> None:
            while True:
                item: ImageItem = self.download_queue.get()
                parse_result: ParseResult = urlparse(item.url)
                item.url: str = "{}://{}{}?{}".format(parse_result.scheme if len(parse_result) > 0 else "https",
                                                      parse_result.netloc, parse_result.path, parse_result.query)
                logger.info("download thread {}: fetch {}".format(self.getName(), item.url))
                download_img_resp = requests.get(item.url, stream=True)
                if download_img_resp.status_code != 200:
                    logger.error("item: {} images download failure, result: {}", item, download_img_resp.text)
                    self.download_queue.task_done()  # 就下载一次了
                    time.sleep(0.3)
                    continue
                try:
                    abs_file = self.output.joinpath(Path(parse_result.path).name)
                    with open(abs_file, "wb") as out_file:
                        shutil.copyfileobj(download_img_resp.raw, out_file)
                    del download_img_resp
                    self.covert2_mp4(abs_file)
                    self.download_queue.task_done()  # 就下载一次了
                    # self.record_queue.put(item)
                except Exception as e:
                    logger.error("failure error: {}".format(e))

        def covert2_mp4(self, out_file: str):
            try:
                # cmd = "ffmpeg -f gif -i {} -pix_fmt yuv420p {}.mp4".format(out_file, out_file)
                cmd = "ffmpeg -f gif -i {} {}.mp4".format(out_file, out_file)
                logger.info("covert gif to mp4: {}".format(cmd))
                os.system(cmd)
            except Exception as e:
                logger.error("covert {} to mp4 failure, err: {}".format(out_file, e.args))

    class Recorder(Thread):
        daemon = True

        def __init__(self, queue: Queue, options: dict, **kwargs):
            super().__init__(**kwargs)
            self.options = options
            self.database = GaoXiaoGifDb(options)
            self.queue = queue

        def run(self) -> None:
            while True:
                item: ImageItem = self.queue.get()
                logger.info("record to sqlite3 db: {}".format(item.url))
                self.database.record(item)  # record to database
                self.queue.task_done()

    def __init__(self, options: dict):
        super(GaoXiaoGif, self).__init__(options)

        queue_size = options.get("queue_size", 1000)
        self.max_count = options.get("count", 1000)
        self.download_queue = Queue(queue_size)
        # self.record_queue = Queue(queue_size)
        download_thread_num = options.get("download_thread_num", 3)
        for index in range(download_thread_num):  # start download threading
            download_thread = self.Downloader(self.download_queue, output=options.get("output", ""),
                                              daemon=True, name="downloader-{}".format(index))
            download_thread.start()
            logger.info("start download thread name: {}".format(download_thread.getName()))

        self.record_db = GaoXiaoGifDb(options)

    def crawl(self):
        try:
            self.browser.get(self.url)
            total_element: WebElement = WebDriverWait(self.browser, self.timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".page  .Total.record"))
            )
            total_page: int = int(total_element.text)
            download_url = self.url
            for cursor in range(total_page):
                if cursor > 0:
                    download_url = self.url + "index_{}.html".format(cursor)
                try:
                    self.explorer(download_url)
                except TimeoutException as e:
                    logger.error("found element timeout: {}".format(e.args))
                except NoSuchElementException as e:
                    logger.error("con't found element: {}".format(e.args))
        finally:
            self.download_queue.join()
            self.export2_videos()
            self.dispose()

    def explorer(self, url, cursor: int = 0) -> None:
        self.browser.get(url)
        image_boxes: List[WebElement] = WebDriverWait(self.browser, self.timeout).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".listgif-box .listgif-giftu p > img"))
        )
        if len(image_boxes) * cursor >= self.max_count:
            logger.info("download arrive target, stop it")
            return None

        for image_box in image_boxes:
            image_url: str = image_box.get_attribute("gifsrc")
            if image_url is None:
                image_url: str = image_box.get_attribute("src")
            if self.record_db.exists(image_url):
                logger.info("image: {} already record in database.".format(image_url))
                continue
            image_desc: str = image_box.get_attribute("alt")
            item = ImageItem(url=image_url, hash_code=image_url, title=image_desc)
            self.record_db.record(item)
            self.download_queue.put(item)

    def export2_videos(self) -> bool:
        current_index: int = self.record_db.current_index()
        videos = self.record_db.rows(current_index)
        videos_export_json(videos, self.options.get("output"))
        max_index: int = self.record_db.max_id()
        self.record_db.truncate_index()
        return self.record_db.record_max_id(max_index)

    def dispose(self):
        self.browser.close()
