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
from selenium.webdriver import Chrome, ChromeOptions
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)


class BiliB(object):
    timeout: int = 0

    browser: Chrome = None

    pub_url: str = "https://member.bilibili.com/v2#/upload/video/frame"

    def __init__(self, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout <= 0:
            timeout = 10
        self.timeout = timeout
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--disabled-plugins-discovery")
        self.browser = Chrome(chrome_options=chrome_options)

    def pub(self, loadfile: str):
        videos = self.load_videos(loadfile=loadfile)
        self.browser.maximize_window()
        self.browser.get(self.pub_url)
        for video in videos:
            logger.info("do upload video: {}".format(video))

    def load_videos(self, loadfile: str) -> Dict[str, Any]:
        videos_file = Path(loadfile)
        if not videos_file.exists():
            raise ValueError("load file not exists")

        with open(loadfile, "r") as fd:
            return json.load(fd, parse_int=True)
