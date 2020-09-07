# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

import urllib

from urllib.parse import urlparse, ParseResult


def main():
    url = "https://f.video.weibocdn.com/000bgUTegx07Gdm8fQnl01041200655h0E010.mp4?label=mp4_hd&template=576x1024.24.0&trans_finger=7c347e6ee1691b93dc7e5726f4ef34b3&ori=0&ps=1CwnkDw1GXwCQx&Expires=1599466813&ssig=if7lN%2B1%2Fxa&KID=unistore,video"
    a: ParseResult = urlparse(url)
    print("{schema}//{hostname}{path}".format(schema=a.scheme, hostname=a.hostname, path=a.path))


if __name__ == '__main__':
    main()
