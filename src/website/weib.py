# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

import logging

from src.website.browser import Browser
from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

logger = logging.getLogger(__name__)


class WeiB(object, Browser):
    name: str = "weibo"

    url: str = "https://weibo.com"

    timeout = 10

    browser: Chrome = None

    def __init__(self, **kwargs):
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--mute-audio")
        if kwargs.get("headless"):
            chrome_options.set_headless()
        self.timeout = kwargs.get("timeout", 10)
        self.browser = Chrome(chrome_options=chrome_options)

    def crawl(self) -> bool:
        self.browser.get(url=self.url)
        self.tab_switch(self.url)
        try:
            videos_elements = WebDriverWait(driver=self.browser, timeout=self.timeout).until(
                EC.presence_of_all_elements_located((By.XPATH, ""))
            )
            if len(videos_elements) <= 0:
                return False

        except NoSuchElementException as e:
            logger.error("element not found: {}".format(e.args[-1]))
            return False
        except TimeoutException as e:
            logger.error("element not found timeout: {}".format(e.args[-1]))
            return False
        finally:
            self.tab_close()
