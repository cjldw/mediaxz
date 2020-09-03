# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

import logging
from selenium.webdriver import Chrome

logger = logging.getLogger(__name__)


class Browser(object):
    browser: Chrome = None

    tabs: dict = {}

    def tab_close(self, tab: str):
        try:
            if not self.tabs.get(tab, None):
                logger.info("browser tab not found: {}".format(tab))
                return None
            self.browser.close()
        except Exception as e:
            logger.error("close browser tab failure, {}".format(e.args[-1]))

    def tab_switch(self, tab: str) -> bool:
        window = self.tabs.get(tab, None)
        if window is not None:
            self.browser.switch_to.window(window)
            return True
        open_windows = self.tabs.values()

        for current_window in self.browser.window_handles:
            if current_window in open_windows:
                continue
            self.tabs.update({tab: current_window})
            self.browser.switch_to.window(current_window)
            return True
        return False

    def tabs_close(self) -> bool:
        for index, tab in self.tabs:
            try:
                self.browser.switch_to.window(tab)
                self.browser.close()
            except Exception as e:
                logger.error("close tab: {} failure, err: {}".format(tab, e.args[-1]))
        return True
