#!/usr/bin/env python
# *-* coding:UTF-8 *-*

"""
# Author: yuyet 
# Date:   2018/1/24
# Description: 昆明大屏展示所需图表的数据, 通过查询启迪MySQL Mongodb 获取到数据, 写入指定文件中,并发送给指定的人
"""

# -------------------
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time
import json
import pymongo
import datetime
import yagmail
from MySQL_db import MysqlDb
from pymongo import MongoClient
# -------------------

today = (datetime.date.today()).strftime("%Y-%m-%d")
statistics_file = "/tmp/chart_%s.txt" % (today)
dbinfo = {
    "host": "172.16.4.4",
    "user": "dev",
    "password": "Chargerlink@com",
    "database": "chargerlink_charger"
}

def chart_two():
    """
    新能源汽车企业接入量 (图二)  新能源汽车类型统计 (图三)
    :return:
    """

    sql1 = """
    SELECT c.comm_name, count(v.vin_code) as car_count
    FROM chargerlink_charger.t_vehicle v JOIN chargerlink_card_manager.t_commercial c 
    ON v.oper_only_mark = c.id  GROUP BY  c.comm_name order by car_count desc
    """

    sql2 = """
    select case when oper_type=1 then '分时租赁车' when oper_type=2 then '公务用户车'  
    when oper_type=3 then '物流车' when oper_type=4 then '大巴车'  else '出租车' end  type, cnt 
    from ( select 1 as oper_type,count(1) as cnt
    from chargerlink_charger.t_vehicle where oper_type=1
    union
    select 2,count(1) as cnt
    from chargerlink_charger.t_vehicle where oper_type=2
    union
    select 3,count(1) as cnt
    from chargerlink_charger.t_vehicle where oper_type=3
    union
    select 4,count(1) as cnt
    from chargerlink_charger.t_vehicle where oper_type=4
    union
    select 5,count(1) as cnt
    from chargerlink_charger.t_vehicle where oper_type=5) t;
    """

    sqls = {u"===新能源汽车企业接入量===": sql1, u"===新能源汽车类型统计===": sql2}

    with MysqlDb(dbinfo) as cur:
        try:
            for title, sql in sqls.iteritems():
                cur.execute(sql)

                with open(statistics_file, "a") as fd:
                    fd.write(title+"\n\n")
                    for line in cur.fetchall():
                        fd.write(str(line[0])+" "+str(line[1])+"\n")
                    fd.write("\n\n")
        except Exception as err:
            print err



def chart_five_six():
    """
    周期故障报警次数(图七)   新能源汽车告警信息(图八)
    :return:
    """
    todayday = int(time.mktime((datetime.date.today()).timetuple()))*1000
    day7ago  = int(time.mktime((datetime.date.today() - datetime.timedelta(days=7)).timetuple()))*1000
    day14ago = int(time.mktime((datetime.date.today() - datetime.timedelta(days=14)).timetuple()))*1000
    day21ago = int(time.mktime((datetime.date.today() - datetime.timedelta(days=21)).timetuple()))*1000
    day28ago = int(time.mktime((datetime.date.today() - datetime.timedelta(days=28)).timetuple()))*1000


    day0 =  (datetime.date.today()).strftime('%Y-%m-%d')
    day7 =  (datetime.date.today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    day14 = (datetime.date.today() - datetime.timedelta(days=14)).strftime('%Y-%m-%d')
    day21 = (datetime.date.today() - datetime.timedelta(days=21)).strftime('%Y-%m-%d')
    day28 = (datetime.date.today() - datetime.timedelta(days=28)).strftime('%Y-%m-%d')

    conn = MongoClient("172.16.4.31", 27017)
    db = conn["monitor"]
    alarm = db.access_alarm_100

    sql1 = '{"createdOn":{"$gt":%s,"$lt":%s}}' % (day28ago, day21ago)
    sql2 = '{"createdOn":{"$gt":%s,"$lt":%s}}' % (day21ago, day14ago)
    sql3 = '{"createdOn":{"$gt":%s,"$lt":%s}}' % (day14ago, day7ago)
    sql4 = '{"createdOn":{"$gt":%s,"$lt":%s}}' % (day7ago, todayday)

    mgs = {sql1: day21, sql2: day14, sql3: day7, sql4: day0}

    with open(statistics_file, "a") as fd:
        fd.write(u"===周期故障告警次数:==="+"\n\n")
        for sql, dy in mgs.iteritems():
            alarm_num = len(alarm.find(json.loads(sql)).distinct('deviceId'))
            line_info = u"七天前至%s的告警次数%s" % (dy, alarm_num)
            fd.write(line_info+"\n")
        fd.write("\n\n")

    # 新能源汽车告警信息(图八) 统计
    sql = '{"createdOn":{"$gt":%s,"$lt":%s}}' % (day21ago, todayday)
    alarms = alarm.find(json.loads(sql)).sort([("createdOn", pymongo.DESCENDING)]).limit(12)

    with MysqlDb(dbinfo) as cur, open(statistics_file, "a") as fd:
        try:
            fd.write(u"===新能源汽车告警信息:==="+"\n\n")
            for alarm_info in alarms:
                print alarm_info['deviceId'], alarm_info['createdOn'], alarm_info['code']
                vin_code = alarm_info['deviceId']
                createtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(alarm_info['createdOn']/1000))
                err_code = alarm_info['code']

                sql = "select oper_type,vehicle_firm,type_name from chargerlink_charger.t_vehicle vt, chargerlink_base_platform.t_car_type_info ct where vt.vehicle_model_num = ct.id and vin_code='%s' limit 1" % vin_code
                cur.execute(sql)
                result = cur.fetchone()
                oper_type = result[0]
                vehicle_firm = result[1]
                car_type = result[2]

                sql = "select alarm_type_name from access_platform.t_dict_alarm_type where alarm_type_id=%s limit 1" % err_code
                cur.execute(sql)
                err_info = cur.fetchone()[0]

                line = "%s %s %s %s %s %s" % (oper_type, car_type, vehicle_firm, err_code, err_info, createtime)
                fd.write(line+'\n')
            fd.write("\n\n")

        except Exception as err:
            print err

    km = db.vehicle_ent_brand_driving
    with open(statistics_file, "a") as fd:
        fd.write((u"===新能源新能源运行统计:==="+"\n\n"))

        brands = [163, 245, 249, 251, 253, 255, 259, 261, 263, 265]
        kmPerDriving = 0
        kmPerDay = 0
        durationPerDriving = 0
        durationPerDay = 0
        timesPerDay = 0

        for brand in brands:
            sql = '{"brand": %s}' % brand
            che = km.find(json.loads(sql)).sort([("time", 1)]).limit(1)

            for car in che:
                if len(car)>0:
                    kmPerDriving = kmPerDriving + car["durationPerDriving"]
                    kmPerDay = kmPerDay + car["kmPerDay"]
                    durationPerDriving = durationPerDriving + car["durationPerDriving"]
                    durationPerDay = durationPerDay + car["durationPerDay"]
                    timesPerDay = timesPerDay + car["timesPerDay"]

        # 最早日期距当前日期差

        km.find({'brand': 257}).sort({'time': -1}).limit(1)
        old_day = datetime.datetime.strptime('2017-05-31', '%Y-%m-%d')
        now_day = datetime.datetime.today()

        day_diff = (now_day - old_day).days

        #line = "次均里程:%s 日均里程:%s  次均时长:%s  日均时长:%s  日均出行次数:%s" % (kmPerDriving, kmPerDay, durationPerDriving, durationPerDay, timesPerDay)
        line = "次均里程:%s \n次均时长:%s \n日均里程:%s \n日均时长:%s \n出行次数:%s \n出行天数:%s \n累计总里程:%s \n日均出行次数:%s" % (kmPerDriving/10.0, durationPerDriving/1000/60.0, kmPerDay/10.0, round(durationPerDay/1000/60.0/60.0), timesPerDay*day_diff, day_diff, kmPerDay*day_diff, timesPerDay)
        fd.write(line+"\n")


    # 最早日期距当前日期差
    # with open(statistics_file, "a") as fd:
    #     old_day = datetime.datetime.strptime('2017-05-31', '%Y-%m-%d')
    #     now_day = datetime.datetime.today()
    #
    #     day_diff = (now_day - old_day).days
    #     line = u"===最早日期距当前日期差%s天" % day_diff
    #     fd.write(line+"\n")


def send_mail():
    """
        将查询记录作为邮件内容发送给 users 中的收件人.
    """
    sendto_users = {'nanyinghao@zhongchuangsanyou.com': "墨色竹青", }   # 收件人列表
    try:
        yag = yagmail.SMTP(user='xian@zhongchuangsanyou.com', password='5IG94slz6NTNZPXj', host='smtp.exmail.qq.com', smtp_ssl=True, port='465')  # 这里要用ssl
        body = u"邮件内容正文."
        yag.send(to=sendto_users, subject=u'昆明大屏图表统计', contents=[body, statistics_file])
    except Exception as e:
        print "发送错误:", e
    else:
        yag.close()
        print u"已发送邮件"


def main():
    chart_two()
    chart_five_six()
    send_mail()


if __name__ == '__main__':
    main()
