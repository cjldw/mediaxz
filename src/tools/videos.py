# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

from typing import List
from pathlib import Path
import shutil
from json import dump
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def videos_export_json(data: List[dict] = None, output: str = None):
    if output is None:
        output = "output"
    download_dir = Path(output)
    if not download_dir.exists():
        download_dir.mkdir(mode=644, parents=True)
    abs_file = download_dir.joinpath("videos.json")
    if abs_file.exists():
        shutil.move(abs_file, download_dir.joinpath(
            "videos.json-{}".format(datetime.now().strftime("%Y%m%d%H%M%S"))))
    with open(abs_file, mode="w", encoding="utf-8") as fd:
        dump(data, fd, indent="  ", ensure_ascii=False)
    logger.info("export all video to videos.json")
