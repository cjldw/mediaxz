#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @title: 
# @author: luowen<loovien@163.com>
# @website: https://loovien.github.com
# @time: 9/5/2020 1:34 AM

import threading
from queue import Queue

q = Queue(100)


def work():
    while True:
        item = q.get()
        print("work {} finished".format(item))
        q.task_done()


def main():
    T = threading.Thread(target=work, daemon=True)
    T.start()

    for item in range(0, 100):
        q.put(item)

    q.join()
    print("end1")
    T.join()

    print("end")


if __name__ == '__main__':
    main()
