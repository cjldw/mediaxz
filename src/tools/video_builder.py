#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @title: 
# @author: luowen<loovien@163.com>
# @website: https://loovien.github.com
# @time: 9/17/2020 10:18 PM

import logging
import time
import ffmpeg
import shutil
import random
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)


class VideoBuilder(object):

    def __init__(self, options: dict):
        self.options = options
        self.bgm = options.get("bgm", None)
        self.source = options.get("source", None)
        self.framerate = options.get("framerate", 0.5)
        self.output = options.get("output", "output.mp4")

    def built(self):
        if not Path(self.source).exists():
            raise ValueError("images source must settings")
        bgm_file = self.get_bgm()
        prob = ffmpeg.probe(str(bgm_file.absolute()))
        bgm_file_info = next((stream for stream in prob["streams"] if stream['codec_type'] == "audio"), None)
        logger.info("background music information: {}".format(bgm_file_info))
        bgm_file_duration = float(bgm_file_info["duration"])

        if bgm_file_duration <= 0:
            raise ValueError("background music invalid, for duration zero")
        video_images_num = int(bgm_file_duration * self.framerate)
        video_file: Path = self.video(video_images_num)
        self.merge_bgm(video_file, bgm_file)
        return True

    def get_bgm(self) -> Path:
        bgm = Path(self.bgm)
        if bgm.is_file():
            return bgm
        files = [file for file in bgm.iterdir() if file.is_file()]
        if len(files) <= 0:
            raise FileNotFoundError("music file not found")
        index = random.randint(0, len(files))
        return files[index - 1]

    def video(self, num: int) -> Path:
        image_files: List[Path] = [file for file in Path(self.source).iterdir() if file.is_file()]
        if num > len(image_files):
            raise ValueError("image numbers not enough")
        tmp_dir = Path(self.source).joinpath("tmp")
        if tmp_dir.exists():
            shutil.move(tmp_dir, Path(self.source).joinpath("tmp-{}".format(time.strftime("%Y%m%d%H%M%S"))))
        tmp_dir.mkdir(mode=644, parents=True)
        for index, image in zip(range(num), image_files[:num]):
            shutil.move(str(image), tmp_dir.joinpath("{}{}".format(index, image.suffix)))
        output = tmp_dir.joinpath("__tmp.mp4")
        ffmpeg.input("{}/%d.jpg".format(str(tmp_dir.absolute())), framerate=self.framerate, format="image2").output(
            filename=str(output)).overwrite_output().run()
        return Path(output)

    def merge_bgm(self, video: Path, audio: Path) -> bool:
        ffmpeg.input(filename=str(video.absolute())).output(ffmpeg.input(str(audio)).audio, self.output, vcodec="copy",
                                                            shortest=None).overwrite_output().run()
        return True
