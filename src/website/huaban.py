#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @title: 
# @author: luowen<loovien@163.com>
# @website: https://loovien.github.com
# @time: 9/14/2020 9:08 PM

import time
import logging
import requests
import re
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
from selenium.webdriver.remote.webdriver import WebElement
from threading import Thread

logger = logging.getLogger(__name__)


class HuaBan(Browser):
    name: str = "huaban"

    url: str = "https://huaban.com/explore/xiaoqingxinmeinv/"

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
                self.download_queue.task_done()  # 就下载一次了
                if download_img_resp.status_code != 200:
                    logger.error("item: {} images download failure, result: {}", item, download_img_resp.text)
                    time.sleep(0.3)
                    continue
                try:
                    img_hash: str = hashlib.md5(item.url.encode("utf-8")).hexdigest()
                    item.hash = img_hash
                    abs_file = self.output.joinpath(img_hash + ".jpg")
                    with open(abs_file, "wb") as out_file:
                        shutil.copyfileobj(download_img_resp.raw, out_file)
                    del download_img_resp
                    # self.record_queue.put(item)
                except Exception as e:
                    logger.error("failure error: {}".format(e))

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
                logger.info("record to sqlite3 db: {}".format(item.url))
                self.database.record(item)  # record to database
                self.queue.task_done()

    def __init__(self, options: dict):
        super(HuaBan, self).__init__(options)
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

        self.record_db = HuaBanDb(options)
        # record_thread = self.Recorder(self.record_queue, options, daemon=True, name="recorder")
        # record_thread.start()
        # logger.info("start record thread name: {}".format(record_thread.getName()))

    def crawl(self):
        try:

            self.explorer()
            self.close()
            return True
        except Exception as e:
            logger.error("huaban explorer failure, err: {}".format(e.args[-1]))
            return False
        finally:
            logger.info("record queue completed")

    def explorer(self):
        try:
            self.last_index_record()
            self.browser.get(self.url)
            self.scrolling(0)
        finally:
            self.download_queue.join()
            # self.record_queue.join()
            logger.info("download, record threading completed")

    def scrolling(self, cursor: int = 0, times: int = 0) -> None:
        if cursor > self.max_count:
            logger.info("crawler arrive user's target.")
            return
        if times >= 3:
            logger.info("cursor: {} times: {} mark as completed".format(cursor, times))
            return
        self.browser.execute_script("window.scrollBy(0, 500)")
        time.sleep(3)
        flow_boxes: List[WebElement] = WebDriverWait(self.browser, self.timeout).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".pin.wfc"))
        )
        element_length = len(flow_boxes)
        if element_length <= 0 or cursor == element_length:
            self.browser.execute_script("window.scrollBy(0, 500)")
            self.scrolling(cursor, times + 1)
            return

        logger.info("flow boxes length: {}".format(len(flow_boxes)))
        for flow_box in flow_boxes:  # explain target ImageItem data and dispatch
            try:
                imgbox: WebElement = flow_box.find_element_by_css_selector(".img.x.layer-view img")
                http_url: str = imgbox.get_attribute("src")
                width: int = int(imgbox.get_attribute("width"))
                height: int = int(imgbox.get_attribute("height"))
                url = re.sub(r'_fw\d+', "_fw1000", http_url).replace("/webp", "/jpeg")
                logger.info("get image url: {}".format(url))
                hash_code = hashlib.md5(url.encode("utf-8")).hexdigest()
                # if self.record_db.exists(hash_code):
                #     logger.info("image: {} download before skip it.".format(url))
                #     continue
                image_item = ImageItem(url=url, width=width, height=height, hash_code=hash_code)
                # self.record_db.record(image_item)
                self.download_queue.put(image_item)
            except Exception as e:
                logger.error("find img address failure, err: {}".format(e.args))
                continue
        cursor += element_length
        logger.info("current num: {} scroll to next page".format(cursor))
        self.scrolling(cursor, 0)

    def download_sub(self, cursor: int = 0, retry_times: int = 0) -> None:
        try:
            if retry_times >= 3 or cursor >= 1200:
                logger.info("cursor: {} scroll {} times, mark as download image completed.".format(cursor, requests))
                return None
            self.browser.execute_script("document.querySelector('.board-pins.cst-scrollbar').scrollBy(0, 600)")
            sub_img_boxes: List[WebElement] = WebDriverWait(self.browser, self.timeout).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cell.x.layer-view.img > img"))
            )
            image_length = len(sub_img_boxes)
            if image_length == cursor:
                self.download_sub(cursor, retry_times + 1)
            for image in sub_img_boxes[cursor: image_length]:
                image_url: str = image.get_attribute("src")
                url = re.sub(r'_fw\d+', "_fw1000", image_url).replace("/webp", "jpeg")
                image_item = ImageItem(url=url)
                logger.info("get image url: {}".format(url))
                self.download_queue.put(image_item)
            return None
            # self.download_sub(image_length, 0)
        except NoSuchElementException as e:
            logger.error("not found sub imgage box: {}".format(e.args))
            self.download_sub(cursor, retry_times + 1)
        except Exception as e:
            logger.error("download subset image not success. {}".format(e.with_traceback(None)))
            self.download_sub(cursor, retry_times + 1)

    def last_index_record(self) -> bool:
        if not self.record_db.record_max_id(self.record_db.max_id()):
            raise RuntimeError("record last max index failure")
        return True

    def close(self):
        for handler in self.tabs:
            self.tab_switch(handler)
