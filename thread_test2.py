#!/usr/bin/env python
# *-* coding:UTF-8 *-*

"""
# Author: yuyet 
# Date:   2018/4/6
# Description:
"""

# -------------------
import threading
import time
# -------------------


class Mythread(threading.Thread):
    """

    """

    def __init__(self, name, age, cnt):
        super(Mythread, self).__init__()
        self.name = name
        self.age = age
        self.cnt = cnt

    def run(self):
        time.sleep(self.cnt)
        print "sleep:%ds %s %s" % (self.cnt, self.name, self.age)


if __name__ == '__main__':

    print "master prom is starting...."
    threads = []

    for i in xrange(5):
        th = Mythread("tom"+str(i), 23, i+1)
        th.start()
        th.join()
    print "master prom is over..."
