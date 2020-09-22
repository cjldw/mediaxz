# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

import hashlib
from datetime import datetime
from typing import Optional


class LiveVideo(object):

    def __init__(self, title: str, url: str, code: Optional[str], created_date: Optional[datetime]):
        self.title = title
        self.url = url
        if not code:
            code = hashlib.md5(url.encode("utf-8")).hexdigest()
        if not created_date:
            created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.code = code
        self.created_date = created_date
