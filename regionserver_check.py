#!/usr/bin/env python
# *-* coding:UTF-8 *-*

"""
# Author: yuyet 
# Date:   2018/1/29
# Description:
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
        isactive1 = resp.json()['beans'][0]["tag.isActiveMaster"]
        deadrs1 = resp.json()['beans'][0]["tag.deadRegionServers"]
        numRegionServers1 = resp.json()['beans'][0]["numRegionServers"]
        numDeadRegionServers1 = resp.json()['beans'][0]["numDeadRegionServers"]
        DeadRegionServers1 = resp.json()['beans'][0]["tag.deadRegionServers"]

    except Exception as e:
        isactive1 = "None"

    try:
        resp = requests.get(url2, timeout=5)
        isactive2 = resp.json()['beans'][0]["tag.isActiveMaster"]
        deadrs2 = resp.json()['beans'][0]["tag.deadRegionServers"]
        numRegionServers2 = resp.json()['beans'][0]["numRegionServers"]
        numDeadRegionServers2 = resp.json()['beans'][0]["numDeadRegionServers"]
        DeadRegionServers2 = resp.json()['beans'][0]["tag.deadRegionServers"]

    except Exception as e:
        isactive2 = "None"


    if isactive1 == "true" or isactive2 == "true":
        if isactive1 == "true":
            if numRegionServers1 == 5 and numDeadRegionServers1 == 0:
                print "Ok all regionservers ok."
            else:
                if DeadRegionServers1.find(";"):
                    deadrs = ";".join([rs for rss in DeadRegionServers1.split(";") for rs in rss.split(",") if "zcsy" in rs])
                elif DeadRegionServers1.find(","):
                    deadrs = DeadRegionServers1.split(",")[0]
                print "Error regionserver %s error." % deadrs

        if isactive2 == "true":
            if numRegionServers2 == 5 and numDeadRegionServers2 == 0:
                print "Ok all regionservers ok."
            else:
                if DeadRegionServers2.find(";"):
                    deadrs = ";".join([rs for rss in DeadRegionServers2.split(";") for rs in rss.split(",") if "zcsy" in rs])
                elif DeadRegionServers2.find(","):
                    deadrs = DeadRegionServers2.split(",")[0]
                print "Error regionserver %s error." % deadrs
    else:
        print "Error Hbase cluster"


if __name__ == '__main__':
    main()
