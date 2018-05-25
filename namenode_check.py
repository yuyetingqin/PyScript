#!/usr/bin/env python
# *-* coding:UTF-8 *-*

"""
# Author: yuyet 
# Date:   2018/1/29
# Description: 检测namenode 的状态
"""

# -------------------
import json
import requests
# -------------------


def main():
        namenode1_url = "http://172.16.4.50:50070/jmx?qry=Hadoop:service=NameNode,name=NameNodeStatus"
        namenode2_url = "http://172.16.4.69:50070/jmx?qry=Hadoop:service=NameNode,name=NameNodeStatus"

        try:
            response = requests.get(namenode1_url, timeout=5)
            namenode1 = response.json()['beans'][0]
            namenode1_state = namenode1['State']
        except Exception as e:
            namenode1_state = 'None'

        try:
            response = requests.get(namenode2_url, timeout=5)
            namenode2 = response.json()['beans'][0]
            namenode2_state = namenode2['State']
        except Exception as e:
            namenode2_state = 'None'

        # print namenode1_state, namenode2_state
        if namenode1_state == "standby" or namenode2_state == "active":
            print "OK Hadoop namenode ok."
        elif namenode2_state == "standby" or namenode1_state == "active":
            print "OK Hadoop namenode ok."
        else:
            print "Error Hadoop namenode state error."


if __name__ == '__main__':
    main()
