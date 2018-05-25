#!/usr/bin/env python
# *-* coding:UTF-8 *-*

"""
# Author: yuyet 
# Date:   2018/4/6
# Description:
"""

# -------------------
import os
import threading
# -------------------

g_num = 500
thread_lock = threading.Lock()


def funadd(num):
    """
    :param num:
    :return:
    """
    global g_num
    lock_flag = thread_lock.acquire(True)
    if lock_flag:
        for i in xrange(num):
            g_num += i
            # g_num -= i
        thread_lock.release()
    print "Fun add result: %s" % g_num


def funsum(num):
    global g_num
    lock_flag = thread_lock.acquire(True)
    if lock_flag:
        for i in xrange(num):
            lock_True = thread_lock.acquire(True)
            # g_num += i
            g_num -= i
        thread_lock.release()
    print "Fun sum result: %s" % g_num


if __name__ == '__main__':
    cnt = 100

    th1 = threading.Thread(target=funadd, args=(cnt,))
    th2 = threading.Thread(target=funsum, args=(cnt,))

    th1.start()
    th2.start()

    print "Finally g_num is %s " % g_num
    print "*"*50
