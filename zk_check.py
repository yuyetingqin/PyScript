#!/usr/bin/env python
# *-* coding:UTF-8 *-*

"""
# Author: yuyet 
# Date:   2018/1/26
# Description: zookeeper 进程检测
"""

# -------------------
from kazoo.client import KazooClient as zkclient
from kazoo.exceptions import ConnectionLoss
# -------------------


def main():
    """
    :return:
    """
    zk = zkclient(hosts='172.16.4.70:2181')

    try:
        zk.start(timeout=10)
        zkflag = zk.ensure_path('/consumers/console-consumer-31283')
        if zkflag:
            print 1
        else:
            print "zk connection error"
    except ConnectionLoss:
        print "zk connection timeout"
    except Exception as e:
        print "zk error " + str(e)


if __name__ == '__main__':
    main()
