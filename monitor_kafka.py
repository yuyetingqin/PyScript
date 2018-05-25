#!/usr/bin/env python
# *-* coding:UTF-8 *-*

"""
# Author: yuyet 
# Date:   2018/3/20
# Description:
"""

# -------------------
import os
import time
from kafka.client import KafkaClient
from kafka.protocol.commit import OffsetFetchRequest_v1, OffsetFetchResponse_v1, OffsetFetchRequest_v0, OffsetFetchResponse_v0
from kafka.protocol.offset import OffsetRequest_v0, OffsetResponse_v0

# -------------------


# 监控的topic
topics = ['zcsy']

# 要监控的groupid
monitor_group_ids = ['consumer_1']

# broker-list
servers = '172.16.4.62:9092'

# 监控数据上报间隔 秒
time_interval = 2.5
# 历史全量数据上报间隔
history_time_interval = 5 * 60


duration = 0
client = None
conn = None
partition_cache = {}
brokers_cache = []
kafka_type = []
zk_type = []



def get_brokers():
    if not brokers_cache:
        brokers = client.cluster.brokers()
        if brokers:
            brokers_cache.extend([x.nodeId for x in brokers])
    return brokers_cache


def get_partitions(topic):
    if not partition_cache or topic not in partition_cache:
        partitions = client.cluster.available_partitions_for_topic(topic)
        if partitions:
            partition_cache[topic] = [x for x in partitions]
        else:
            return []
    return partition_cache[topic]


def get_logsize():
    """
        获取topic 下每个partition的logsize(各个broker的累加)
    :return:
    """
    tp = {}  # topic : partition_dict
    brokers = get_brokers()
    for topic in topics:
        partitions = get_partitions(topic)
        pl = {}  # partition : logsize
        for broker in brokers:
            # 这里取笛卡尔积可能有问题,但是不影响parse中解析了
            for partition in partitions:
                print broker, partition
                client.send(broker, OffsetRequest_v0(replica_id=-1, topics=[(topic, [(partition, -1, 1)])]))
                responses = client.poll()
                print responses
                pdict = parse_logsize(topic, partition, responses)
                print pdict
                append(pl, pdict)
        tp[topic] = pl
    return tp


def append(rdict, pdict):
    if rdict:
        # 已经有记录,累加
        for k, v in pdict.items():
            if k in rdict:
                rdict[k] = rdict[k] + v
            else:
                rdict[k] = v
    else:
        rdict.update(pdict)


def parse_logsize(t, p, responses):
    """
    单个broker中单个partition的logsize
    :param responses:
    :param p:
    :param t:
    :return:
    """
    for response in responses:
        if not isinstance(response, OffsetResponse_v0):
            return {}
        tps = response.topics
        topic = tps[0][0]
        partition_list = tps[0][1]
        partition = partition_list[0][0]
        # 异步poll来的数据可能不准
        if topic == t and partition == p and partition_list[0][1] == 0:
            logsize_list = partition_list[0][2]
            logsize = logsize_list[0]
            return {partition: logsize}
    return {}


def parse_offsets(t, responses):
    dr = {}
    for response in responses:
        if not isinstance(response, (OffsetFetchResponse_v1, OffsetFetchResponse_v0)):
            return {}
        tps = response.topics
        topic = tps[0][0]
        partition_list = tps[0][1]
        if topic == t:
            for partition_tunple in partition_list:
                if partition_tunple[3] == 0:
                    offset = partition_tunple[1]
                    dr[partition_tunple[0]] = offset
    return dr


def get_offsets():
    # {gid: dict}
    gd = {}
    for gid in monitor_group_ids:
        td = {}  # {topic:dict}
        for topic in topics:
            pd = {}  # {partition:dict}
            for broker in get_brokers():
                partitions = get_partitions(topic)
                if not partitions:
                    return {}
                else:
                    responses = optionnal_send(broker, gid, topic, partitions)
                    dr = parse_offsets(topic, responses)
                    append(pd, dr)
            td[topic] = pd
        gd[gid] = td
    return gd


def optionnal_send(broker, gid, topic, partitions):
    if gid in kafka_type:
        return kafka_send(broker, gid, topic, partitions)
    elif gid in zk_type:
        return zk_send(broker, gid, topic, partitions)
    else:
        responses = zk_send(broker, gid, topic, partitions)
        dct = parse_offsets(topic, responses)
        if is_suitable(dct):
            zk_type.append(gid)
            return responses
        responses = kafka_send(broker, gid, topic, partitions)
        dct = parse_offsets(topic, responses)
        if is_suitable(dct):
            kafka_type.append(gid)
        return responses


def is_suitable(dct):
    for x in dct.values():
        if x != -1:
            return True


def kafka_send(broker, gid, topic, partitions):
    client.send(broker, OffsetFetchRequest_v1(consumer_group=gid, topics=[(topic, partitions)]))
    return client.poll()


def zk_send(broker, gid, topic, partitions):
    client.send(broker, OffsetFetchRequest_v0(consumer_group=gid, topics=[(topic, partitions)]))
    return client.poll()



def do_task():
    offset_dict = get_offsets()
    logsize_dict = get_logsize()
    for gk, gv in offset_dict.items():
        for tk, tv in gv.items():
            for pk, pv in tv.items():
                if logsize_dict and tk in logsize_dict:
                    dr = logsize_dict[tk]  # partition:logsize
                    if dr and pk in dr:
                        param = (gk, tk, pk, pv, dr[pk],
                                 time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                        # print param
    print "-"*50
                        # store_db(param)


if __name__ == "__main__":
    client = KafkaClient(bootstrap_servers=servers, request_timeout_ms=3000)
    while True:
        do_task()
        time.sleep(time_interval)
        duration += time_interval


