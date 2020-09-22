# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:


import logging
import ffmpeg

from src.db.live_video_db import LiveStreamDb
from pathlib import Path

logger = logging.getLogger(__name__)


class StreamLive(object):

    def __init__(self, options: dict):
        self.options = options
        self.database = LiveStreamDb(options)

    def stream(self) -> str:
        locale_file = self.options.get("source", None)
        if locale_file is not None and len(locale_file) > 0:
            return str(locale_file)
        last_index = self.database.last_playing()
        return self.database.video_url(last_index)

    def live(self, times: int):
        daemon = self.options.get("daemon")
        input_url = self.stream()
        output_url = self.options.get("url")
        if times >= 5:
            logger.error("failure times max than 5， stop")
            return None
        try:
            ffmpeg.input(input_url).output(ffmpeg.input(output_url)).run()
        except Exception as e:
            logger.error("publish url: {} to {} failure, {}".format(input_url, output_url, e))
            if daemon:
                return self.live(times=times + 1)
        if daemon:
            return self.live(0)
