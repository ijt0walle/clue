# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 10:45:03 2017

@author: DawnBreeze
"""

import pymssql
import pandas as pd
import pymysql as MySQLdb
import sys
import datetime as dt
import time
import datetime

# import calendar as cl
reload(sys)
sys.setdefaultencoding('utf8')


def get_data_100(start_day, end_day):
    conn = pymssql.connect(host="192.168.171.100", user="sa", password="t123456", charset="utf8")
    sql = '''
    SELECT
        ts_id,
          ts_line_number,
        ts_start_time,
        ts_dialing,
        ts_duration
    FROM
        MyRecData.dbo.bill
    WHERE
        --len(ts_dialing)>5 AND 
     ts_start_time>='%s' AND
     ts_start_time<'%s'  AND
     ts_directions='拨出' ;
    ''' % (start_day, end_day)
    aa1 = pd.read_sql(sql, conn)
    aa1['fm_line'] = 100
    del conn
    return aa1


def get_data_177(start_day, end_day):
    conn = pymssql.connect(host="192.168.171.177", user="sa", password="t123456", charset="utf8")
    sql = '''
    SELECT
        ts_id,
          ts_line_number,
        ts_start_time,
        ts_dialing,
        ts_duration
    FROM
        MyRecData.dbo.bill
    WHERE
        --len(ts_dialing)>5 AND 
     ts_start_time>='%s' AND
     ts_start_time<'%s'  AND
     ts_directions='拨出' ;
    ''' % (start_day, end_day)
    aa2 = pd.read_sql(sql, conn)
    aa2['fm_line'] = 177
    del conn
    return aa2


def put_data(aa):
    mysql_conn = MySQLdb.connect(host='121.43.168.132', user='maxwell', port=3307,
                                 passwd='ED81A84EC3B290A4EFA26122test', db='sale_phone', charset="utf8")
    # cursor=mysql_conn.cursor()
    # sql='''drop table sale_phone.phone_dialing '''
    # cursor.execute(sql)
    sql = """CREATE TABLE if not exists sale_phone.phone_dialing (
              `ts_id` int(11) DEFAULT NULL COMMENT '原数据库拨打id',
              `ts_line_number` int(11) DEFAULT NULL COMMENT '拨打线路',
              `ts_start_time` datetime DEFAULT NULL COMMENT '拨打时间',
              `ts_dialing` varchar(100) DEFAULT NULL COMMENT '拨打电话',
              `ts_duration` varchar(100) DEFAULT NULL COMMENT '通话时长',
              `fm_line` int(11) DEFAULT NULL COMMENT '来源：100/177',
              unique KEY (ts_id,fm_line)
            ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='出发地数据表';"""
    # sql='''drop table sale_phone.phone_dialing '''
    # cursor.execute(sql)
    aa.to_sql('phone_dialing', mysql_conn, flavor='mysql', schema='sale_phone', index=False, if_exists='replace',
              chunksize=10000)
    del mysql_conn






