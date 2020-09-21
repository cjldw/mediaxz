# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

import ffmpeg
import traceback
from PIL import ImageFont, ImageDraw, Image
from pathlib import Path
import shutil
import click
import glob


def image():
    with open("../output/fc68997c9c27b1a47ff7a9c0e9b9dc1d.jpg", mode="rb") as fd:
        img1 = Image.open(fd)
        img_width, img_height = img1.size
        offset_x = int((960 - img_width) / 2)
        offset_y = int((img_height - 600) / 1.65)

        offset_x = offset_x if offset_x > 0 else 0
        offset_y = offset_y if offset_y > 0 else 0

        corp_width = img_width if img_width <= 960 else 960
        corp_height = img_height if img_height <= 600 else 600
        corp_img = img1.crop((0, offset_y, corp_width, offset_y + corp_height))

        img2 = Image.new(mode="RGB", size=(960, 600), color="white")
        img2.paste(corp_img, (offset_x, 0))
        img2.save("xx.jpg")


def rename():
    files = glob.glob("../dist/output/huaban/tmp/*")
    for index in range(len(files)):
        file_path = Path(files[index])
        file_path.rename(Path(file_path.parent).joinpath("c9_{}.jpg".format(index)))


def ok() -> bool:
    try:
        print(111)
        raise ValueError("not int")
    except ValueError as e:
        traceback.print_list()
        return False
    finally:
        print("finally")


def video_mk():
    tmp_dir = Path("../dist/output/huaban/tmp")
    output = tmp_dir.joinpath("__tmp.mp4")
    ffmpeg.input("{}/%d.jpg".format(str(tmp_dir.absolute())), framerate=1, format="image2").output(
        filename=str(output)).overwrite_output().run()


def bgm_merge():
    audio = ffmpeg.input("../dist/test/1.mp3")
    ffmpeg.input("../dist/output/huaban/tmp/__tmp.mp4").output(audio, "merge.mp4", vcodec="copy", shortest=None).run()


def merge():
    s = ffmpeg.concat(
        ffmpeg.input("../dist/test/3.mp4"),
        ffmpeg.input("../dist/test/2.mp4"),
        n=2,
        v=1,
        a=1,
    )
    audio2 = ffmpeg.input("../dist/test/2.ape")
    audio1 = ffmpeg.input("../dist/test/1.mp3") \
        # .filter("join", inputs=2, channel_layout="stereo").output( "333.mp3").run()
    ffmpeg.filter((audio2, audio1), "join", inputs=2, channel_layout="stereo").output(
        "xxx.mp3").overwrite_output().run()
    # audio = ffmpeg.input("../dist/test/1.mp3")
    # video = ffmpeg.input("../dist/test/3.mp4")
    # ffmpeg.filter((audio,), 'join', inputs=1, channel_layout="stereo") \
    #     .output(video.video, "xxx.mp4", shortest=None, vcodec="copy").overwrite_output()
    # ffmpeg.input("../dist/test/3.mp4").output(ffmpeg.input("../dist/test/1.mp3"), "./output.mp4", shortest=None,
    #                                           vcodec="copy").overwrite_output().run()

    # ffmpeg.filter((ffmpeg.input("../dist/test/1.mp3"),), 'join', inputs=1).output(
    #     ffmpeg.input("../dist/test/3.mp4").video,
    #     "output.mp4", vcodec="copy").run()
    # print("xx")
    # ffmpeg.output(filename="demo.mp4", codec="copy").run()


if __name__ == '__main__':
    # bgm_merge()
    # video_mk()
    rename()
    # merge()
    # a = ok()
    # a = ok()
    # print(a)
    # value = click.prompt("Please input a valid integer value: ", type=int)
    # print(value)
    #
    # if click.confirm("Do you want continue?", prompt_suffix="😀", show_default=True, abort=False):
    #     click.echo("hehe, you sb")
