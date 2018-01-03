# coding=utf-8
import time
import traceback
import signal

import os

import sys

from flow import flow
from mysql_db import Mysql_db
from login_chrome import login_chrome_1688


IP = '17'
region = '上海'
all_classi = '母婴'
url_region = 'province=%C9%CF%BA%A3'
user_password = None

def get_user_name():
    my_sql = Mysql_db()
    sql = "select id,user_name,pass_word from test.crm_clue_password where status = 0 and ip = '%s' limit 1" % IP;
    result = my_sql.get_sql_data(sql)
    if result is None or len(result) == 0:
        return result
    sql = "update test.crm_clue_password set status = 1 where id = " + str(result[0][0]);
    my_sql.update(sql)
    return result[0]

def processing():
    user_password = get_user_name()

    if user_password is None or len(user_password) == 0:
        user_password = (123456, 'flesdewe234', 'lqz123456789')
    try:
        print user_password
        if user_password is None or len(user_password) == 0:
            print 'user name and pass word is over'
            return
        request = login_chrome_1688(user_password[1], user_password[2], int(user_password[0]))
        time.sleep(3)
        while True:
            try:
                f = flow(request,region,all_classi,url_region)
                f.search_classi()
                time.sleep(360)
            except Exception as e:
                print 'traceback.format_exc():\n%s' % traceback.format_exc()
    finally:
        my_sql = Mysql_db()
        sql = "update test.crm_clue_password set status = 0 where id = " + str(user_password[0]);
        my_sql.excute(sql)


def onsignal_term(a, b):
    print '收到SIGTERM信号'
    try:
        if (int(user_password[0]) - 123456) != 0:
            sql = "update test.crm_clue_password set status = 0 where id = " + str(user_password[0]);
            print 'sql = '+ str(sql)
            Mysql_db().excute(sql)
    except:
        print 'traceback.format_exc():\n%s' % traceback.format_exc()
    finally:
        sys.exit()



if __name__ == '__main__':
    print 'pid = '+ str(os.getpid())
    signal.signal(signal.SIGTERM, onsignal_term)
    processing()
