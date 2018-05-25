#!/usr/bin/env python
# *-* coding:UTF-8 *-*

"""
@date

统计阿里云 histore 数据库中各个分区表在08 - 12 月分的记录数
"""

# -------------------
import calendar
import datetime
import mysql.connector
# -------------------

def lastday(n):
    """
    返回给定月份的最后一天日期
    :param n:
    :return:
    """
    day_num = calendar.monthrange(datetime.date.today().year, n)[1]
    return day_num


def main():
    """

    :return:
    """
    dbinfo = {
        "host": "drdsvfi6tdpr7k65public.drds.aliyuncs.com",
        "user": "xianevdata_drds",
        "password": "_Histore4cpp",
        "database": "xianevdata_drds"
    }

    # histore 中的表
    tables = ["alarm_data", "charge_device_temp", "charge_device_voltage", "engine_data", "extreme_value", "fuel_cell", "motor_data", "vehicle_data", "vehicle_login_record", "vehicle_package_log", "vehicle_position"]

    try:
        conn = mysql.connector.connect(**dbinfo)
        cur = conn.cursor()

        for table in tables:
            sql = "select count(*) from %s where datatime>='2017-08-01 00:00:00' and datatime<='2017-12-31 23:59:59'" % table
            cur.execute(sql)

            title_num = cur.fetchone()
            print "%s 08-12月分,记录总数：%s" % (table, title_num[0])

            for monthnum in xrange(8, 13): # 统计 8 - 12 月的分区表记录
                start_date = "2017-%s-01 00:00:00" % str(monthnum)
                end_date = "2017-%s-%s 23:59:59" % (str(monthnum).zfill(2), lastday(monthnum))

                sql = "select count(*) from %s where datatime>='%s' and datatime<='%s' " % (table, start_date, end_date)
                # print sql
                cur.execute(sql)
                title_num = cur.fetchone()
                print "%s_%s 月份,记录数：%s" % (table, str(monthnum).zfill(2), title_num[0])

            print ""

    except mysql.connector.Error as err:
        print err
    else:
        cur.close()
        conn.close()


if __name__ == '__main__':
    main()

