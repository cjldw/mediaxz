# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:


import mder
import requests

url = "https://omts.tc.qq.com//ApV-LotHRNTGplf-VcHR0asAXgVVMQbjSTLqrDOOEAz8/uwMROfz2r5xgoaQXGdGnC2df645GziNP4fCTXzcc9dfItw5M/p3gjsqhXgu74ajbe-I3tjTOBz2zUcAucQSocT82wyboK_Q-k4N9mrFl6S9jwJu5MaJ6GBWY6MqWiVAlC0ubIHMd1k7zU4GoTvPeyNdghrqjUXRYQYIyFcA9BvhhnUrXS4lMQX_pG0-mOLwa4WaOcxg/l003033vcms.321002.ts.m3u8?ver=4"


def main():
    response = requests.get(url)

    # with open("demo.m3u8", "w+") as file:
    #     file.write(response.text)
    playlist = mder.m3u8_downloader(m3u8_file_path="./demo.m3u8",
                                    temp_file_path="./")  # this could also be an absolute filename
    # playlist = m3u8.loads()
    playlist.start()


# if you already have the content as string, use

if __name__ == '__main__':
    main()
