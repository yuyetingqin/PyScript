#!/usr/bin/env python
# *-* coding:UTF-8 *-*

"""
# Author: yuyet 
# Date:   2018/4/4
# Description:
"""

# -------------------
from kazoo.client import KazooClient
import json
from MySQL_db import MysqlDb
# -------------------


def get_master_status():
    """
    获取MySQL 主节点的binlog 日志信息
    :return:
    """
    dbinfo = {
        "host": "172.16.4.100",
        "user": "repluser",
        "password": "replabc",
        "port": 3309,
    }
    binlog_file = None
    binlog_position = None

    sql = "show master status;"
    with MysqlDb(dbinfo) as cur:
        try:
            cur.execute(sql)
            binlog_info = cur.fetchall()
            if binlog_info[0]:
                # print binlog_info[0]
                binlog_file = binlog_info[0][0]
                binlog_position = binlog_info[0][1]
        except Exception as err:
            print err

    return binlog_file, binlog_position


def main():
    """

    :return:
    """
    zk = KazooClient(hosts='172.16.4.50:2181', read_only=True, timeout=10)
    zk.start()

    # 检查更新进度
    if zk.exists("/otter/canal/destinations/evbase/1001/cursor"):
        # Print the version of a node and its data
        data = zk.get("/otter/canal/destinations/evbase/1001/cursor")[0]
        journalname = (json.loads(data)["postion"]["journalName"])
        position = (json.loads(data)["postion"]["position"])

        binlog_file, binlog_position = get_master_status()

        if journalname != binlog_file or (binlog_position - position) > 8000:
            print "Please check the canal service."
        else:
            print 1
    else:
        print "Canal Error."

    zk.stop()


if __name__ == '__main__':
    main()
