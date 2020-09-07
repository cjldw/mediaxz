# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

from __future__ import annotations

import logging
import json
from typing import List, Any, Optional, Dict
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

    pub_url: str = "https://member.bilibili.com/v2#/upload/video/frame"

    def __init__(self, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None or timeout <= 0:
            timeout = 10
        self.timeout = timeout
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--disabled-plugins-discovery")
        self.browser = Chrome(chrome_options=chrome_options)

    def pub(self):
        download_dir = setting_get("download_output")
        loadfile = Path(download_dir).joinpath("videos.json")
        if not loadfile.exists():
            raise ValueError("load file not exists")
        with open(loadfile, mode="r", encoding="utf-8") as fd:
            videos = json.load(fd)
        if len(videos) <= 0:
            logger.error("video is empty. dont nothing ")
            return False
        self.browser.maximize_window()
        self.browser.get(self.pub_url)
        tip: str = input("are you login [Y/N]>> ")
        if tip.lower() != 'y':
            logger.error("don't login yet.")
            return False
        self.browser.get(self.pub_url)
        for video in videos:
            WebDriverWait(self.browser, self.timeout).until(
            )
            logger.info("do upload video: {}".format(video))
