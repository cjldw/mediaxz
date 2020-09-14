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
from src.config import configs

logger = logging.getLogger(__name__)


@click.group()
def entrance():
    pass


@entrance.command()
@click.option('--website', type=click.Choice(["weibo", "xinpianchang"], case_sensitive=False), default="weibo",
              help="which website to crawl")
@click.option("--db", default="./mediaxz.db", help="database file path")
@click.option("--count", default=30, help="number of video crawl")
def download(**kwargs):
    config_logging()
    configs.update(kwargs)
    if configs.get("website") == WeiB.name:
        weibo = WeiB(configs)
        if not weibo.crawl():
            logger.error("crawl https://webo.cn failure")
            return False
        return True
    logger.error("application crawl not implement yet.")


@entrance.command()
@click.option("--target", type=click.Choice(["bili", "weibo"], case_sensitive=False), default="bili",
              help="which website to upload")
@click.option("--from", default="微博", help="video copy from")
def upload(**kwargs) -> bool:
    configs.update(kwargs)
    bili = BiliB(configs)
    bili.pub()
    return True


def launch():
    click.CommandCollection(sources=[entrance])()


if __name__ == '__main__':
    launch()
