# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

import re
from urllib.parse import urlparse, ParseResult


def pure_url(url: str) -> str:
    result: ParseResult = urlparse(url=url)
    return "{schema}://{hostname}{path}".format(schema=result.scheme, hostname=result.hostname, path=result.path)


def pure_title(title: str) -> str:
    try:
        index_l = title.strip(" ").index("L")
        return title[0:index_l]
    except ValueError as e:
        return title


def remove_emoji(string: str) -> str:
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)
