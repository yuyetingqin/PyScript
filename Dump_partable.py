#!/usr/bin/env python
# *-* coding:UTF-8 *-*
"""

"""

# -------------------
import os
import subprocess

# -------------------


def inport_data(sqlfile):
    """

    :param sqlfile:
    :return:
    """
    sql = "mysql -uroot -pzcsy_x168 -e'use rdata; source %s;'" % sqlfile

    try:
        proc = subprocess.Popen(sql, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        outinfo, errinfo = proc.communicate()

        print "Outinfo:", outinfo
        print "Errinfo:", errinfo

    except Exception as e:
        print e


def main():
    """
    按天导出列表中各分区表的数据到本地目录
    :return:
    """
    tables = ["charge_device_temp", "charge_device_voltage", "extreme_value", "vehicle_data", "vehicle_position"]
    start_date = "2017-12-%s 00:00:00"
    end_date = "2017-12-%s 23:59:59"
    sql = """mysqldump -hdrdsvfi6tdpr7k65public.drds.aliyuncs.com -uxianevdata_drds -p_Histore4cpp --default-character-set=utf8 --net_buffer_length=10240 --no-create-db --skip-add-locks  xianevdata_drds charge_device_temp --where=" dataTime>='%s' and dataTime<='%s'"  > /home/tm_mysql/data/sql/%s_%s.sql"""

    try:
        for table_name in tables:
            for dt in xrange(1, 32):
                dt = str(dt).zfill(2)
                sdate = start_date % dt
                edate = end_date % dt
                sqlcmd = sql % (sdate, edate, table_name, dt)
                print sqlcmd

                proc = subprocess.Popen(sqlcmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                outinfo, errinfo = proc.communicate()

                print "Outinfo:", outinfo
                print "Errinfo:", errinfo

    except Exception as e:
        print e


if __name__ == '__main__':
    main()
