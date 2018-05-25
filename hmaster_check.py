#!/usr/bin/env python
# *-* coding:UTF-8 *-*

"""
# Author: yuyet 
# Date:   2018/1/29
# Description: 检测 hmaster 的状态
"""

# -------------------
import os
import json
import requests
# -------------------


def main():
    url1 = "http://172.16.4.71:16010/jmx?qry=Hadoop:service=HBase,name=Master,sub=Server"
    url2 = "http://172.16.4.72:16010/jmx?qry=Hadoop:service=HBase,name=Master,sub=Server"

    try:
        resp = requests.get(url1, timeout=5)
        host_name = resp.json()['beans'][0]["tag.Hostname"]
        isactive = resp.json()['beans'][0]["tag.isActiveMaster"]

        # print host_name, type(isactive)
        if isactive == "false":
            print "Ok Hmaster %s is backup." % host_name
        elif isactive == "true":
            print "Ok Hmaster %s is active." % host_name
        else:
            print "Error Hmaster error."

    except Exception as e:
        print "Error hmaster error."


if __name__ == '__main__':
    main()
