#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @title: 
# @author: luowen<loovien@163.com>
# @website: https://loovien.github.com
# @time: 9/17/2020 10:41 PM

import ffmpeg
import unittest

from pathlib import Path
from src.tools.video_builder import VideoBuilder


class TestVideoBuilder(unittest.TestCase):

    def setUp(self) -> None:
        self.video_builder = VideoBuilder(options={"bgm": "../dist/bgm/", "source": "../dist/output/huaban"})

    def test_bgm_info(self):
        bgm = self.video_builder.get_bgm()
        print(bgm)

    def test_video_info(self):
        # prob = ffmpeg.probe(Path(self.video_builder.bgm).absolute())
        prob = ffmpeg.probe(str(Path("../dist/bgm/beatifully.ape").absolute()))
        bgm_file_info = next((stream for stream in prob["streams"] if stream['codec_type'] == "audio"), None)
        print(bgm_file_info)

    def test_video_merge_bgm(self):
        a = Path("../dist/test/luowen.jpg")
        self.video_builder.merge_bgm(Path("../dist/test/3.mp4"), Path("../dist/test/1.mp3"))
