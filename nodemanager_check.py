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
    url1 = "http://zcsy-hdp-70:8088/jmx?qry=Hadoop:service=ResourceManager,name=ClusterMetrics"
    url2 = "http://zcsy-hdp-71:8088/jmx?qry=Hadoop:service=ResourceManager,name=ClusterMetrics"

    try:
        rspon = requests.get(url2, timeout=5)
        nm_num2 = rspon.json()["beans"][0]["NumActiveNMs"]
        # print nm_num2
    except Exception as e:
        nm_num2 = 0

    try:
        rspon = requests.get(url1, timeout=5)
        nm_num1 = rspon.json()["beans"][0]["NumActiveNMs"]
        # print nm_num1
    except Exception as e:
        nm_num1 = 0


    if nm_num1 == 5 or nm_num2 == 5:
        print "Ok all nodemanager ok."
    else:
        print "Error nodemanager error."


if __name__ == '__main__':
    main()
