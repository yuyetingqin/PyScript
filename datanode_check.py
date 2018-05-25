#!/usr/bin/env python
# *-* coding:UTF-8 *-*

"""
# Author: yuyet 
# Date:   2018/1/29
# Description: 检测datanode
"""

# -------------------
import json
import requests
# -------------------


def main():

    namenode1_url = "http://172.16.4.50:50070/jmx?qry=Hadoop:service=NameNode,name=NameNodeStatus"
    datanode1_url = "http://172.16.4.50:50070/jmx?qry=Hadoop:service=NameNode,name=FSNamesystemState"
    deadnode1_url = "http://172.16.4.50:50070/jmx?qry=Hadoop:service=NameNode,name=NameNodeInfo"

    namenode2_url = "http://172.16.4.69:50070/jmx?qry=Hadoop:service=NameNode,name=NameNodeStatus"
    datanode2_url = "http://172.16.4.69:50070/jmx?qry=Hadoop:service=NameNode,name=FSNamesystemState"
    deadnode2_url = "http://172.16.4.69:50070/jmx?qry=Hadoop:service=NameNode,name=NameNodeInfo"

    try:
        try:
            response = requests.get(namenode1_url, timeout=5)
            namenode1_state = response.json()['beans'][0]['State']
        except Exception as e:
            namenode1_state = "None"

        try:
            response = requests.get(namenode2_url, timeout=5)
            namenode2_state = response.json()['beans'][0]['State']
        except Exception as e:
            namenode2_state = "None"

        if namenode1_state == "active":
            response = requests.get(datanode1_url, timeout=5)
            datanode1_live = response.json()['beans'][0]['NumLiveDataNodes']
            datanode1_dead = response.json()['beans'][0]['NumDeadDataNodes']

            if datanode1_live == 5 and datanode1_dead == 0:
                print "Ok all datanode ok."
            else:
                response = requests.get(deadnode1_url, timeout=5)
                deadnodes = response.json()['beans'][0]['DeadNodes']
                deadnodes = ";".join([k.split(":")[0] for k in json.loads(deadnodes).keys()])
                print "Error %s datanode dead." % deadnodes

        elif namenode2_state == "active":
            response = requests.get(datanode2_url, timeout=5)
            datanode2_live = response.json()['beans'][0]['NumLiveDataNodes']
            datanode2_dead = response.json()['beans'][0]['NumDeadDataNodes']

            if datanode2_live == 5 and datanode2_dead == 0:
                print "Ok all datanode ok."
            else:
                response = requests.get(deadnode2_url, timeout=5)
                deadnodes = response.json()['beans'][0]['DeadNodes']
                deadnodes = ";".join([k.split(":")[0] for k in json.loads(deadnodes).keys()])
                print "Error %s datanode dead." % deadnodes
        else:
            print "Error namenode is dead or namenode state is error."

    except Exception as e:
        print "Error Hadoop datanode error info: %s." % (str(e))


if __name__ == '__main__':
    main()
