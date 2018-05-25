#!/usr/bin/env python
# *-* coding:UTF-8 *-*

"""
# Author: yuyet 
# Date:   2018/1/29
# Description:
"""

# -------------------
import json
import requests
# -------------------


def main():
    namenode1_url = "http://172.16.4.50:50070/jmx?qry=Hadoop:service=NameNode,name=NameNodeStatus"
    journalnode1_url = "http://172.16.4.50:50070/jmx?qry=Hadoop:service=NameNode,name=NameNodeInfo"

    namenode2_url = "http://172.16.4.69:50070/jmx?qry=Hadoop:service=NameNode,name=NameNodeStatus"
    journalnode2_url = "http://172.16.4.69:50070/jmx?qry=Hadoop:service=NameNode,name=NameNodeInfo"

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
            response = requests.get(journalnode1_url, timeout=5)
            journal_info = response.json()['beans'][0]['NameJournalStatus']

            journal_info = json.loads(journal_info)[0]['manager']

            if "172.16.4.50:8485" in journal_info and "172.16.4.69:8485" in journal_info and "172.16.4.70:8485" in journal_info:
                print "Ok journalnode all ok."
            else:
                print "Error journalnode error %s ." % journal_info

        elif namenode2_state == "active":
            response = requests.get(journalnode2_url, timeout=5)
            journal_info = response.json()['beans'][0]['NameJournalStatus']

            journal_info = json.loads(journal_info)[0]['manager']

            if "172.16.4.50:8485" in journal_info and "172.16.4.69:8485" in journal_info and "172.16.4.70:8485" in journal_info:
                print "Ok journalnode all ok."
            else:
                print "Error journalnode error %s ." % journal_info
        else:
            print "Error journalnode error ."

    except Exception as e:
        print "Error Hadoop journalnode error info: %s." % (str(e))


if __name__ == '__main__':
    main()
