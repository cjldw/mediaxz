# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:


import logging
import os
from src.tools.notify import Reporting
from src.db.live_video_db import LiveStreamDb

logger = logging.getLogger(__name__)


class StreamLive(object):
    default_stream = "rtmp://live-push.bilivideo.com/live-bvc/?streamname=live_505797972_44307093&key=69f49942956030afd257668fee1f5497&schedule=rtmp"

    def __init__(self, options: dict):
        self.options = options
        self.database = LiveStreamDb(options)
        self.reporting = Reporting()

    def stream(self) -> str:
        locale_file = self.options.get("source", None)
        if locale_file is not None and len(locale_file) > 0:
            return str(locale_file)
        last_index = self.database.last_playing()
        video_info = self.database.video_info(last_index)
        affected_rows = self.database.delete_record_index()
        logger.info("delete videos stream index records affected rows: {}".format(affected_rows))
        affected_rows = self.database.record_index(video_info[0])
        logger.info("fetch video info: {} record stream index affected rows: {}".format(video_info, affected_rows))
        return video_info[1]

    def live(self) -> None:
        times = 0
        daemon = self.options.get("daemon")
        output_url = self.options.get("url", self.default_stream)
        while True:
            input_url = self.stream()
            logger.info("input url: {}, output url: {}".format(input_url, output_url))
            if times >= 5:
                self.reporting.sender("发现错误超过5次， 停止")
                logger.error("failure times max than 5， stop")
                times = 0
                continue
            try:
                cmd = "ffmpeg -re -i \"{}\" -codec copy -f flv \"{}\"".format(input_url, output_url)
                logger.info("execute command: {}".format(cmd))
                os.system(cmd)
                # ffmpeg.input(input_url).output(ffmpeg.input(output_url)).run()
            except Exception as e:
                times += 1
                logger.error("publish url: {} to {} failure, {}".format(input_url, output_url, e))
            if not daemon:
                logger.info("live don't run with daemon, stop")
                return None
            logger.info("live url: {} completed, switch to next".format(input_url))
