# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

from PIL import ImageFont, ImageDraw, Image
from pathlib import Path
import shutil
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
    files = glob.glob("../output/huaban/*")
    for index in range(len(files)):
        file_path = Path(files[index])
        file_path.rename(Path(file_path.parent).joinpath("{}.jpg".format(index)))


if __name__ == '__main__':
    rename()
