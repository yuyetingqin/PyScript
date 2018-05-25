#!/usr/bin/env python
# *-* coding:UTF-8 *-*

"""
# Author: yuyet 
# Date:   2018/1/15
# Desc:
"""

# -------------------
import os
import time
import threading
# -------------------

num = 0
lock = threading.Lock()
semaphore = threading.BoundedSemaphore(3)

class MyThread(threading.Thread):
    def __init__(self, name, lock):
        super(MyThread, self).__init__(name=name)
        self.sema = lock

    def run(self):
        global num

        # self.lock.acquire()
        self.sema.acquire()
        for i in xrange(10000):
            num += 1
            num -= 1

        print "子线程: %s, 运行结果为: %s" % (self.name, num)
        # self.lock.release()
        self.sema.release()



if __name__ == '__main__':
    threads = []
    for i in xrange(20):
        th = MyThread("thread"+str(i), semaphore)
        th.start()
        # th.join()

    # for th in threads:
    #     th.join()
    time.sleep(2)
    print "主线程结束..."
