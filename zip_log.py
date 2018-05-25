#!/usr/bin/env python
# *-* coding:UTF-8 *-*

"""
# Author: yuyet 
# Date:   2018/4/12
# Description:
"""

# -------------------
import os
import zipfile
import fnmatch
import datetime
# -------------------



class Ziplogfile(object):
    """
    __getlogfile

    """
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")

    def __init__(self, logpath, ziplog):
        self.__logpath = logpath
        self.__loglist = []
        self.__ziplog = ziplog

    # 获取 Logpath 目录下的所有符合条件的日志名称
    def __getlogfile(self):
        for logname in os.listdir(self.__logpath):

            if logname.startswith("info-") and fnmatch.fnmatch(logname, "info-%s.log.[0-9]*" % self.yesterday):
                print logname
                self.__loglist.append(logname)
            elif logname.startswith("spring.log.") and fnmatch.fnmatch(logname, "spring.log.[0-9]*"):
                print logname
                self.__loglist.append(logname)
            elif logname.startswith("error-") and fnmatch.fnmatch(logname, "error-%s.log.[0-9]*" % self.yesterday):
                print logname
                self.__loglist.append(logname)
            elif logname.startswith("consumer-error-") and fnmatch.fnmatch(logname, "consumer-error-%s.log" % self.yesterday):
                print logname
                self.__loglist.append(logname)

            elif logname.startswith("consumer-info-") and fnmatch.fnmatch(logname, "consumer-info-%s.log" % self.yesterday):
                print logname
                self.__loglist.append(logname)

    # 删除日志
    def __deletelogfile(self):
        for logname in self.__loglist:
            os.remove(os.path.join(self.__logpath, logname))

    # 压缩日志文件
    def __ziplogfile(self):
        with zipfile.ZipFile(self.__ziplog, "w") as myzip:
            for logname in self.__loglist:
                myzip.write(os.path.join(self.__logpath, logname))
    #
    def startzip(self):
        self.__getlogfile()
        self.__ziplogfile()
        self.__deletelogfile()


if __name__ == '__main__':
    zf = Ziplogfile(r"d:\evbase", r"d:\evwork\ziplog.zip" )
    zf.startzip()


