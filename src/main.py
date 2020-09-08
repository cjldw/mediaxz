# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

import click
import logging
from src.website.weib import WeiB
from src.logs import config_logging
from src.pub.bilib import BiliB

logger = logging.getLogger(__name__)


@click.command()
@click.option('--website', type=click.Choice(["weibo", "douyu"], case_sensitive=False), default="weibo",
              help="which website to crawl")
@click.option("--upload", type=click.Choice(["bili", "weibo"], case_sensitive=False), default="bili",
              help="which website to upload")
@click.option("--count", default=30, help="number of video crawl")
def main(website: str, **kwargs):
    config_logging()

    bili = BiliB()
    bili.pub()
    return True

    if website == WeiB.name:
        weibo = WeiB(**kwargs)
        if not weibo.crawl():
            logger.error("crawl https://webo.cn failure")
            return False
        # bili = BiliB()
        # bili.pub()
        return True
    logger.error("application crawl not implement yet.")


if __name__ == '__main__':
    main()
