# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

import logging
import time

from typing import List
from src.website.browser import Browser
from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from src.models.video import Video
from src.record import Recoder

logger = logging.getLogger(__name__)


class WeiB(Browser):
    name: str = "weibo"

    browser: Chrome = None

    def __init__(self, options: dict):
        self.count = options.get("count", 10)
        self.url = options.get("url", "https://weibo.com/?category=10011")
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--disable-plugins-discovery")
        if options.get("headless"):
            chrome_options.headless = True
        self.timeout = options.get("timeout", 10)
        self.browser = Chrome(chrome_options=chrome_options)
        self.options = options

    def crawl(self) -> bool:
        self.browser.maximize_window()
        self.browser.get(url=self.url)
        self.tab_switch(self.url)
        try:
            WebDriverWait(self.browser, 100).until(  # wait for weibo platform check redirect and index loaded
                EC.presence_of_element_located((By.ID, "plc_main"))
            )
            self.browser.get(url=self.url)
            self.query_video_element(0)
            return True
        except NoSuchElementException as e:
            logger.error("element not found: {}".format(e.args[-1]))
            return False
        except TimeoutException as e:
            logger.error("element not found timeout: {}".format(e.args[-1]))
            return False
        finally:
            self.tab_close(self.url)
            Recoder.acquire(self.options).export_json()
            Recoder.acquire(self.options).dispose()

    def query_video_element(self, cursor: int) -> bool:
        self.browser.execute_script("window.scrollBy(0, 1000)")
        videos_elements = WebDriverWait(driver=self.browser, timeout=self.timeout).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".UG_list_v2.clearfix"))
        )
        videos_elements_length = len(videos_elements)
        logger.info("current page video length: {}".format(videos_elements_length))
        if videos_elements_length <= 0:
            return False
        if videos_elements_length <= cursor:
            self.browser.execute_script("window.scrollBy(0, 1000)")
            time.sleep(3)
            self.query_video_element(cursor)
            return True

        items: List[WebElement] = videos_elements[cursor:videos_elements_length]
        for video_element in items:
            try:
                video_title_element: WebElement = video_element.find_element_by_css_selector("h3.list_title_s")
                video_url_element: WebElement = video_element.find_element_by_css_selector("h3.list_title_s > a")
                video_img_src_element: WebElement = video_element.find_element_by_css_selector(".vid.W_piccut_v img")

                video_play_element = video_element.find_element_by_css_selector(".vid.W_piccut_v")
                ActionChains(self.browser).move_to_element(video_play_element).click().perform()
                video_src_element: WebElement = video_element.find_element_by_tag_name("video")

                video_title: str = video_title_element.text if video_title_element is not None else ""
                video_title = video_title.replace("#", "").replace("\n", "")
                video_url: str = video_url_element.get_attribute("href")
                video_img_src: str = video_img_src_element. \
                    get_attribute("src") if video_img_src_element is not None else ""
                video_src: str = video_src_element.get_attribute("src") if video_src_element is not None else ""

                logger.info("current video title: {} img_src:{}, video_src: {}".format(
                    video_title,
                    video_img_src,
                    video_src,
                    video_url
                ))
                item = Video(title=video_title, img_src=video_img_src, src=video_src, href=video_url)
                Recoder.acquire(self.options).dispatch_video(item)
                logger.info("dispatch: {} to download task job".format(item.src))

            except NoSuchElementException as e:
                logger.error("video element not found play element: {}".format(e.args[-1]))
                continue
            except TimeoutException as e:
                logger.error("video element find play element timeout: {}".format(e.args[-1]))
                continue

        if videos_elements_length >= self.count:
            logger.info("crawl count arrive config count: {}".format(self.count))
            return True
        cursor = videos_elements_length
        self.browser.execute_script("window.scrollBy(0, 1000)")
        time.sleep(3)
        self.query_video_element(cursor)
