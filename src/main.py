# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

import click

from src.website.weib import WeiB
from src.logs import config_logging


@click.command()
@click.option('--website', type=click.Choice(["weibo", "douyu"], case_sensitive=False), default="weibo",
              help="which website to crawl")
@click.option("--count", default=30, help="number of video crawl")
def main(website: str, **kwargs):
    config_logging()
    if website == WeiB.name:
        weibo = WeiB(**kwargs)
        return weibo.crawl()
    raise ValueError("website {} not implemented".format(website))


if __name__ == '__main__':
    main()
