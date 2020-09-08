# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

from __future__ import annotations

import logging
import json
from typing import List, Any, Optional, Dict
from PIL import Image
from pathlib import Path
from src.config import setting_get
from selenium.webdriver import Chrome, ChromeOptions
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time

logger = logging.getLogger(__name__)


class BiliB(object):
    timeout: int = 0

    browser: Chrome = None

    login_url: str = "https://passport.bilibili.com/login"

    pub_url: str = "https://member.bilibili.com/video/upload.html"

    def __init__(self, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None or timeout <= 0:
            timeout = 10
        self.timeout = timeout
        self.download_dir = Path(setting_get("download_output"))
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--disabled-plugins-discovery")
        self.browser = Chrome(chrome_options=chrome_options)

    def pub(self):
        loadfile = self.download_dir.joinpath("videos.json")
        if not loadfile.exists():
            raise ValueError("load file not exists")
        with open(loadfile, mode="r", encoding="utf-8") as fd:
            videos_ups = json.load(fd)
        if len(videos_ups) <= 0:
            logger.error("video is empty. dont nothing ")
            return False
        self.browser.maximize_window()
        self.browser.get(self.login_url)
        tip: str = input("are you login [Y/N]>> ")
        if tip.lower() != 'y':
            logger.error("don't login yet.")
            return False
        for item in videos_ups:
            try:
                self.browser.get(self.pub_url)
                code = item.get("code", "")
                abs_mp4file = self.download_dir.joinpath(code + ".mp4")
                if not abs_mp4file.exists():
                    logger.error("mp4 file:{} not found, skip it data: {}".format(abs_mp4file, item))
                    continue
                upload_element: WebElement = WebDriverWait(self.browser, self.timeout).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@name='buploader']")))
                # ActionChains(self.browser).move_to_element(upload_element).click().perform()
                # print(upload_element.get_attribute("name"), upload_element.get_attribute("type"))
                upload_element.send_keys(str(abs_mp4file.absolute()))
                time.sleep(10)  # 确保视频上传完成
                img_covert_element: WebElement = WebDriverWait(self.browser, self.timeout).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='cover-v2-preview']/input[@type='file']")))
                if not self.gen_pub_image(code):
                    logger.error("cover image generate failure")
                    continue
                cover_file = self.download_dir.joinpath(code + ".cover.jpg")
                img_covert_element.send_keys(str(cover_file.absolute()))
                time.sleep(3)  # 确保图片上传完成
                confirm_button_element: WebElement = WebDriverWait(self.browser, self.timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".cover-chop-modal-v2-btn")))
                ActionChains(self.browser).move_to_element(confirm_button_element).click().perform()

                selector_element: WebElement = WebDriverWait(self.browser, self.timeout).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, ".select-box-v2-container .select-box-v2-controller")))
                selector_element.click()

                selector_daily_element: WebElement = WebDriverWait(self.browser, self.timeout).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, ".drop-cascader-list-wrp .drop-cascader-list-item"))
                )
                selector_daily_element.click()

                title_element: WebElement = WebDriverWait(self.browser, self.timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".input-box-v2-1-instance > input"))
                )
                title_element.send_keys(item.get("title", "搞笑视频"))

                tags_elements: List[WebElement] = WebDriverWait(self.browser, self.timeout).until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, ".content-tag-v2-other-tag-wrp > .label-item-v2-2-container")))

                if len(tags_elements) >= 4:
                    tags_elements[3].click()
                else:
                    tags_elements[0].click()

                submit_element: WebElement = WebDriverWait(self.browser, self.timeout).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, ".submit-button-group-v2-container > .submit-btn-group-add")))

                ActionChains(self.browser).move_to_element(submit_element).click().perform()
                time.sleep(5)
            except TimeoutException as e:
                logger.error("find submit button timeout: {}".format(e.args[-1]))
                continue
            except NoSuchElementException as e:
                logger.error("not found submit button: {}".format(e.args[-1]))
                continue
        self.browser.close()
        logger.info("do upload video: {}".format(item))

    def gen_pub_image(self, code: str) -> bool:
        img_file = self.download_dir.joinpath(code + ".jpg")
        if not img_file.exists():
            return False
        with open(img_file, "rb") as fd:
            dist_img = Image.open(fd)
            img_width, img_height = dist_img.size
            offset_x = int((960 - img_width) / 2)
            offset_y = int((img_height - 600) / 1.65)

            offset_x = offset_x if offset_x > 0 else 0
            offset_y = offset_y if offset_y > 0 else 0

            corp_width = img_width if img_width <= 960 else 960
            corp_height = img_height if img_height <= 600 else 600
            corp_img = dist_img.crop((0, offset_y, corp_width, offset_y + corp_height))

            background = Image.new(mode="RGB", size=(960, 600), color="white")
            background.paste(corp_img, (offset_x, 0))
            background.save(self.download_dir.joinpath(code + ".cover.jpg"))
        return True
