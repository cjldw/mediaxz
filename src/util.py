# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

from urllib.parse import urlparse, ParseResult


def pure_url(url: str) -> str:
    result: ParseResult = urlparse(url=url)
    return "{schema}//{hostname}{path}".format(schema=result.scheme, hostname=result.hostname, path=result.path)
