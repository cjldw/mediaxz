# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc:

import click

from src.website.weib import WeiB


@click.command()
@click.option('--website', type=click.Choice(["weibo", "douyu"], case_sensitive=False), default="weibo",
              help="which website to crawl")
def main(website: str, **kwargs):
    if website == WeiB.name:
        weibo = WeiB()
        return weibo.crawl()
    raise ValueError("website {} not implemented".format(website))


if __name__ == '__main__':
    main()
