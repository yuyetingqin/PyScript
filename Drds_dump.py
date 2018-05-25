#!/usr/bin/env python
# *-* coding:UTF-8 *-*
"""
查询 histo 中的表，写道本地磁盘上
"""

# -------------------
import os
import mysql.connector
from mysql.connector import errorcode
# -------------------


def main():
    dbinfo = {
        "host": "drdsvfi6tdpr7k65public.drds.aliyuncs.com",
        "user": "xianevdata_drds",
        "password": "_Histore4cpp",
        "database": "xianevdata_drds"
    }
    i = 0

    try:
        conn = mysql.connector.connect(**dbinfo)
        cur = conn.cursor()

        sql = "select * from  charge_device_voltage_201712_0  where datatime>='2017-12-01 00:00:00' and datatime<='2017-12-31 23:59:59' "
        cur.execute(sql)

        with open("e:/charge_device_voltage.txt", "w") as fd:
            for (orgseq, vehiclemodelseq, vehicleseq, districtseq, datatime, rechargeablestoragesubseq, rechargeablestoragevoltage, rechargeablestorageelectric, sumbatterysingle ,firstbatteryseq, sumsinglebattery, singlebatteyvoltage) in cur:
                line = "%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s\n" % (orgseq, vehiclemodelseq, vehicleseq, districtseq, datatime, rechargeablestoragesubseq, rechargeablestoragevoltage, rechargeablestorageelectric, sumbatterysingle, firstbatteryseq, sumsinglebattery, singlebatteyvoltage)
                fd.write(line)
                i += 1
                if i % 500000 == 0:
                    print "line %s flush..." % i
                    fd.flush()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cur.close()
        conn.close()


if __name__ == '__main__':
    main()
