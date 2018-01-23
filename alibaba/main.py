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
regions = ['深证','上海','杭州','广州','南京','苏州']
url_regions= ['city=%C9%EE%DB%DA&province=%B9%E3%B6%AB','province=%C9%CF%BA%A3','city=%BA%BC%D6%DD&province=%D5%E3%BD%AD','city=%B9%E3%D6%DD&province=%B9%E3%B6%AB','city=%C4%CF%BE%A9&province=%BD%AD%CB%D5','city=%CB%D5%D6%DD&province=%BD%AD%CB%D5']
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
        for i in range(0,len(regions)):
            region = regions[i]
            url_region = url_regions[i]
            for all_classi in get_all_classi():
                print 'region = %s, all class = %s' % (region,all_classi[0])
                try:
                    f = flow(request,region,all_classi[0],url_region)
                    f.process_classi()
                    time.sleep(1)
                except Exception as e:
                    print 'traceback.format_exc():\n%s' % traceback.format_exc()
    finally:
        my_sql = Mysql_db()
        sql = "update test.crm_clue_password set status = 0 where id = " + str(user_password[0]);
        my_sql.excute(sql)

def get_all_classi():
    sql = "select class_1 from crm_config group by class_1"
    return Mysql_db().get_sql_data(sql)

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
    '''注册信号'''
    print 'pid = '+ str(os.getpid())
    signal.signal(signal.SIGTERM, onsignal_term)
    processing()
