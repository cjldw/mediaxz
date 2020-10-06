# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

import time
import requests
import logging

logger = logging.getLogger(__name__)


def title_gen() -> str:
    try:
        url = "https://pyq.shadiao.app/api.php"
        response = requests.get(url)
        return response.text
    except Exception as e:
        logger.error("fetch shaidiao title failure, err: {}".format(e.args))
    return "今天没有文案，因为想不出来了. {}".format(time.strftime("%Y-%m-%d %H:%M:%S"))
