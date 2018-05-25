#!/usr/bin/env python
# *-* coding:UTF-8 *-*

"""
# Author: yuyet 
# Date:   2018/4/7
# Description:
"""

# -------------------
import threading
from Queue import Queue
import time
# -------------------

qu = Queue()


class Produc(threading.Thread):
    def __init__(self, num):
        super(Produc, self).__init__()
        self.num = num

    def run(self):
        for i in xrange(self.num):
            q_size = qu.qsize()
            while True:
                if q_size > 10:
                    time.sleep(1)
                    q_size = qu.qsize()
                else:
                    break
            qu.put("生产 新产品" + str(i))


class Consumer(threading.Thread):
    def run(self):
        while True:
            q_size = qu.qsize()
            if q_size != 0:
                msg = qu.get()
                print "消费 %s" % msg
            else:
                print "消费结束..."
                break



if __name__ == '__main__':

    cnt = 100

    thp = Produc(cnt)
    thp.start()

    thc = Consumer()
    thc.start()

