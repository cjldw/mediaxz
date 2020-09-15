# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

import click
import logging
from src.crawl import CrawlFactory
from src.logs import config_logging
from src.pub.bilib import BiliB
from src.config import configs

logger = logging.getLogger(__name__)


@click.group()
def entrance():
    pass


@entrance.command()
@click.option('--website', type=click.Choice(["weibo", "huaban", "xinpianchang"], case_sensitive=False),
              default="weibo", help="which website to crawl")
@click.option("--output", default=".", help="the path of media output ")
@click.option("--db", default="mediaxz.db", help="database file path")
@click.option("--count", default=30, help="number of video crawl")
def download(**kwargs):
    config_logging()
    configs.update(kwargs)
    factory = CrawlFactory(configs).crawl()
    if not factory.crawl():
        logger.error("crawl https://webo.cn failure")
        return False
    return True


@entrance.command()
@click.option("--target", type=click.Choice(["bili", "weibo"], case_sensitive=False), default="bili",
              help="which website to upload")
@click.option("--output", default=".", help="the path of media output ")
@click.option("--copy", type=click.BOOL, default=False, help="copy from other website or not")
@click.option("--classify", default="生活", help="classify of video")
@click.option("--sub-classify", default="搞笑", help="subset classify of video")
def upload(**kwargs) -> bool:
    configs.update(kwargs)
    bili = BiliB(configs)
    bili.pub()
    return True


def launch():
    click.CommandCollection(sources=[entrance])()


if __name__ == '__main__':
    launch()
