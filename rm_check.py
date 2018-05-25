#!/usr/bin/env python
# *-* coding:UTF-8 *-*

"""
# Author: yuyet 
# Date:   2018/1/29
# Description: 检测 rm 的进程的状态  Hadoop:service=ResourceManager,name=ClusterMetrics
"""

# -------------------
import os
import time
import threading
# -------------------


def fun(num):
    time.sleep(3)
    print "%s-线程 %s" % (threading.current_thread().name, num)
    time.sleep(3)


if __name__ == '__main__':
    print "主线程测试开始..."
    thread_list = []
    for i in xrange(6):
        th = threading.Thread(target=fun, args=(i+1,), name="Thread%s" % i)
        thread_list.append(th)

    for thd in thread_list:
        # thd.setDaemon(False)
        thd.start()
        # thd.join()

    while True:
        th_length = len(threading.enumerate())

        print "当前线程数：%s" % th_length
        time.sleep(2)
        if th_length <= 1:
            break

    print "主线程测试结束了..."
