# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

from __future__ import annotations

import logging
import json
import shutil
import time
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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)


class BiliB(object):
    timeout: int = 0

    browser: Chrome = None

    login_url: str = "https://passport.bilibili.com/login"

    pub_url: str = "https://member.bilibili.com/video/upload.html"

    def __init__(self, options: dict):
        timeout = options.get("timeout")
        if timeout is None or timeout <= 0:
            timeout = 10
        self.timeout = timeout
        self.download_dir = Path(setting_get("download_output"))
        self.options = options
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--disabled-plugins-discovery")
        self.browser = Chrome(chrome_options=chrome_options)
        self.browser.execute_script(
            "window.alert = window.confirm = window.prompt = window.onbeforeunload = function() {}")  # ignor

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
        username_element: WebElement = WebDriverWait(self.browser, self.timeout).until(
            EC.presence_of_element_located((By.ID, "login-username")))
        password_element: WebElement = WebDriverWait(self.browser, self.timeout).until(
            EC.presence_of_element_located((By.ID, "login-passwd")))

        username_element.send_keys(18767169856)
        password_element.send_keys("")
        tip: str = input("[........] waiting for login: [Y/N]>> ")
        if tip.lower() != 'y':
            logger.error("don't login yet.")
            return False
        for item in videos_ups:
            try:
                self.browser.get(self.pub_url)
                time.sleep(2)
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
                time.sleep(2)  # 确保图片上传完成
                confirm_button_element: WebElement = WebDriverWait(self.browser, self.timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".cover-chop-modal-v2-btn")))
                ActionChains(self.browser).move_to_element(confirm_button_element).click().perform()

                time.sleep(0.3)
                # 转载处理
                from_element: WebElement = WebDriverWait(self.browser, self.timeout).until(
                    EC.presence_of_element_located(
                        (By.XPATH,
                         "//div[@class='copyright-v2-check-radio-wrp']/div[@class='check-radio-v2-container'][2]")
                    )
                )
                ActionChains(self.browser).move_to_element(from_element).move_to_element(from_element).click().perform()
                time.sleep(1)
                from_text_element: WebElement = WebDriverWait(self.browser, self.timeout).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR,
                         ".copyright-v2-source-input-wrp .input-box-v2-1-container .input-box-v2-1-instance input")
                    )
                )
                from_text_element.send_keys(item.get("href", "微博"))
                selector_element: WebElement = WebDriverWait(self.browser, self.timeout).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, ".select-box-v2-controller")))
                ActionChains(self.browser).move_to_element(selector_element).click().perform()
                time.sleep(1)
                top_selector_elements: List[WebElement] = WebDriverWait(self.browser, self.timeout).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, "//div[@class='drop-cascader-pre-wrp']/div[@class='drop-cascader-pre-item']")))

                for top_selector in top_selector_elements:
                    if top_selector.text == "生活":
                        ActionChains(self.browser).move_to_element(top_selector).click().perform()
                        break
                time.sleep(0.3)
                son_selector_elements: List[WebElement] = WebDriverWait(self.browser, self.timeout).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, "//div[@class='drop-cascader-list-wrp']/div[@class='drop-cascader-list-item']")))
                son_selected: bool = False
                for son_selector in son_selector_elements:
                    if son_selector.text.startswith("搞笑"):
                        ActionChains(self.browser).move_to_element(son_selector).click().perform()
                        son_selected = True
                        break
                if not son_selected:
                    son_default_selector: List[WebElement] = WebDriverWait(self.browser, self.timeout).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//div[@class='drop-cascader-list-wrp']/div[@class='drop-cascader-list-item']")))
                    ActionChains(self.browser).move_to_element(son_default_selector).click().perform()

                title_element: WebElement = WebDriverWait(self.browser, self.timeout).until(
                    EC.presence_of_element_located(
                        (By.XPATH,
                         "//div[@class='content-title-v2-input-wrp']//div[@class='input-box-v2-1-instance']/input")
                    )
                )
                try:
                    title_element.send_keys(Keys.BACKSPACE * 80)
                    title_element.send_keys(item.get("title"))
                    # code_js = """
                    #         let e = document.querySelector("div.input-box-v2-1-instance input.input-box-v2-1-val");
                    #         if (e != null)
                    #             e.value = "{title}";
                    # """.format(title=item.get("title"))
                    # self.browser.execute_script(code_js)
                except Exception as e:
                    title_element.send_keys("无聊真香: {}".format(time.strftime("%Y%m%d %H:%M:%S")))
                    logger.error("set title failure, err: {}".format(e.args[-1]))

                tags_elements: List[WebElement] = WebDriverWait(self.browser, self.timeout).until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, ".content-tag-v2-other-tag-wrp > .label-item-v2-2-container")))
                time.sleep(1.5)
                if len(tags_elements) >= 4:
                    tags_elements[3].click()
                else:
                    tags_elements[0].click()

                submit_element: WebElement = WebDriverWait(self.browser, self.timeout).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, ".submit-button-group-v2-container > .submit-btn-group-add")))

                ActionChains(self.browser).move_to_element(submit_element).click().perform()
                self.mark_as_completed(code)
                time.sleep(5)
            except TimeoutException as e:
                logger.error("find submit button timeout: {}".format(e.args[-1]))
                continue
            except NoSuchElementException as e:
                logger.error("not found submit button: {}".format(e.args[-1]))
                continue
            except Exception as e:
                logger.error("unknow exception: {}".format(e.args))
                continue
            logger.info("do upload video: {}".format(item))
        self.browser.close()

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

    def mark_as_completed(self, code: str) -> bool:
        mp4_file = self.download_dir.joinpath(code + ".mp4")
        if not mp4_file.exists():
            return False
        shutil.move(str(mp4_file), str(self.download_dir.joinpath(code + ".mp4.bak")))
        return True
