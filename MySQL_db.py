#!/usr/bin/env python
# *-* coding:UTF-8 *-*

"""
# Author: yuyet 
# Date:   2018/1/24
# Description:
"""

# -------------------
import mysql.connector
# -------------------


class MysqlDb(object):
    """
        mysql上下文管理
    """
    def __init__(self, dbinfo=None):
        self.dbinfo = dbinfo
        self.conn = None
        self.cur = None

    def getCursor(self):
        self.conn = mysql.connector.connect(**self.dbinfo)
        if self.conn:
            self.cur = self.conn.cursor()

    def closeDb(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.commit()
            self.conn.close()

    def __enter__(self):
        self.getCursor()
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            print "Exception has generate: ", exc_val
            print "Mysql execute error!"
        self.closeDb()


if __name__ == '__main__':
    pass
