#!/usr/bin/env python
# *-* coding:UTF-8 *-*
"""
"""

import yagmail
import datetime
import phoenixdb
import phoenixdb.cursor


def statistic_hbase():
    """
        通过phonexi 接口查询v_report表记录数
    """
    database_url = 'http://localhost:8765/'
    msg = u"截至当前的记录统计：\n"

    try:
        conn = phoenixdb.connect(database_url, autocommit=True)
        cursor = conn.cursor()
        yesterday = (datetime.date.today()+datetime.timedelta(days=-1)).strftime("%Y-%m-%d")+ ' 00:00:00'
        today_time = datetime.date.today().strftime('%Y-%m-%d')+ ' 00:00:00'

        sql="select count(*) from V_REPORT where update_time>= TO_TIMESTAMP('%s') and update_time < TO_TIMESTAMP('%s') " % (yesterday,today_time)
        cursor.execute(sql)
        count = str(cursor.fetchone()[0])
        msg = msg + u"昨天新增记录总数: " + count+"\n"
        print u"昨天新增记录总数: ", count

        sql="select count(*) from V_REPORT where update_time>= TO_TIMESTAMP('%s')" % (today_time,)
        cursor.execute(sql)
        count = str(cursor.fetchone()[0])
        msg = msg + u"今天新增记录总数: "+ count+"\n"
        print u"今天新增记录总数: ", count
        

        sql="select count(*) from V_REPORT"
        cursor.execute(sql)
        count = str(cursor.fetchone()[0])
        msg = msg + u"总记录数: "+ count
        print u"总记录数: ", count
    except Exception:
        msg = msg + " Error."
    return msg


def main():
    """
        获取phonex中的查询记录, 将查询记录作为邮件内容发送给 users 中的收件人.
    """
    users = {'nanyinghao@zhongchuangsanyou.com':"墨色竹青", }
    try:
        yag = yagmail.SMTP(user='xian@zhongchuangsanyou.com', password='5IG94slz6NTNZPXj', host='smtp.exmail.qq.com', smtp_ssl=True, port='465')
        body = statistic_hbase()
        yag.send(to=users, subject='Hbase V_REPORT表统计', contents=[body,])
    except Exception as e:
        print "发送错误:", e
    else:
        yag.close()
        print u"已发送邮件" 


if __name__ == '__main__':
    main()
