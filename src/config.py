# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

from typing import Any, Optional, Union

configs = {
    "queue_size": 10000,
    "download_thread_num": 3,
    "download_output": "./output",
    "timeout": 5,
}


def setting_get(key: str) -> Optional[Union[str, int, dict, tuple, list]]:
    global configs
    items = key.split(".")
    target = None
    for cursor in range(0, len(items)):
        key_seg = items[cursor]
        target = configs.get(key_seg, None)
        if isinstance(target, dict) or isinstance(target, tuple) or isinstance(target, list):
            configs = target
            continue
        return target
    return target
