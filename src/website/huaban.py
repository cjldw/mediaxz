#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @title: 
# @author: luowen<loovien@163.com>
# @website: https://loovien.github.com
# @time: 9/14/2020 9:08 PM

import time
import logging
import requests

import hashlib
import shutil
from typing import List
from pathlib import Path
from queue import Queue
from urllib.parse import urlparse, ParseResult
from src.website.browser import Browser
from src.models.image import ImageItem
from src.db.huaban_image_db import HuaBanDb
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from threading import Thread

logger = logging.getLogger(__name__)


class HuaBan(Browser):
    name: str = "huaban"

    url: str = "https://huaban.com/explore/xiaoqingxinmeinv/"

    class Downloader(Thread):
        daemon = True

        def __init__(self, download_queue: Queue, record_queue: Queue, output: str, **kwargs):
            if len(output) <= 0:
                raise ValueError("download output directory not setting")
            self.download_queue = download_queue
            self.record_queue = record_queue
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
                download_img_resp = requests.get(item.url, stream=True)
                if download_img_resp.status_code != 200:
                    logger.error("item: {} images download failure, result: {}", item, download_img_resp.text)
                    self.download_queue.task_done()
                    time.sleep(0.3)
                    continue
                img_hash: str = hashlib.md5(item.url).hexdigest()
                item.hash = img_hash
                abs_file = self.output.joinpath(img_hash + ".webp")
                with open(abs_file, "wb") as out_file:
                    shutil.copyfileobj(download_img_resp.raw, out_file)
                del download_img_resp
                self.record_queue.put(item)

    class Recorder(Thread):
        daemon = True

        def __init__(self, queue: Queue, options: dict, **kwargs):
            super().__init__(**kwargs)
            self.options = options
            self.database = HuaBanDb(options)
            self.queue = queue

        def run(self) -> None:
            while True:
                item: ImageItem = self.queue.get()
                self.database.record(item)  # record to database
                self.queue.task_done()

    def __init__(self, options: dict):
        super(HuaBan, self).__init__(options)
        queue_size = options.get("queue_size", 1000)
        self.max_count = options.get("count", 1000)
        self.download_queue = Queue(queue_size)
        self.record_queue = Queue(queue_size)
        download_thread_num = options.get("download_thread_num", 3)
        for index in range(download_thread_num):  # start download threading
            download_thread = self.Downloader(self.download_queue, self.record_queue, output=options.get("output", ""),
                                              daemon=True, name="downloader")
            download_thread.start()
        record_thread = self.Recorder(self.record_queue, options, daemon=True, name="recorder")
        record_thread.start()

    def crawl(self):
        try:
            self.explorer()
            self.built_videos()
        except Exception as e:
            logger.error("huaban explorer failure, err: {}".format(e.args))
        finally:
            logger.info("record queue completed")

    def explorer(self):
        try:
            self.scrolling(0)
        finally:
            self.download_queue.join()
            self.record_queue.join()
            logger.info("download, record threading completed")

    def scrolling(self, cursor: int = 0) -> None:
        self.browser.get(self.url)
        flow_boxes: List[WebElement] = WebDriverWait(self.browser, self.timeout).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".pin.wfc"))
        )
        element_length = len(flow_boxes)
        if element_length <= 0:
            self.browser.execute_script("window.scrollBy(0, 500)")
            self.scrolling(cursor)

        for flow_box in flow_boxes:  # explain target ImageItem data and dispatch
            img_box_element = flow_box.find_element_by_css_selector(".img.x.layer-view.loaded > img")
            img_item: ImageItem = ImageItem(url=img_box_element.get_attribute("src"),
                                            width=img_box_element.get_attribute("width"),
                                            height=img_box_element.get_attribute("height"))
            logger.info("fetch image: {} scheduler download".format(str(img_item)))
            self.download_queue.put(img_item)
        if cursor >= self.max_count:
            logger.info("arrive crawl target count")
            return None
        cursor = element_length
        logger.info("scroll to nex page")
        self.browser.execute_script("window.scrollBy(0, 500")
        self.scrolling(cursor)

    def built_videos(self):
        pass
