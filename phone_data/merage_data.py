# coding=utf-8
import datetime
import traceback

from shanghai_phone_data import get_data_100, get_data_177, put_data
import time

from shenzheng_chrome_login import login_chrome_phone
from shenzheng_phone_data import get_phone


while (True):
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=91)
    start_time = '2017-09-01'+ ' 00:00:00'
    end_time = str(today) + ' 00:00:00'
    # start_day_h = dt.datetime.now() - dt.timedelta(days=90)
    # last_day_h = dt.datetime.now()  # 设置结束时间到当前运行时间长度
    print (start_time, end_time)
    try:
        print 'shanghai data .........'
        a100 = get_data_100(start_time, end_time)
        a177 = get_data_177(start_time, end_time)
        aa = a100.append(a177)
        aa = aa.reset_index(drop=1)
        put_data(aa)

        print 'shenzheng data.........'
        yesterday = today - datetime.timedelta(days=5)
        start_time = str(yesterday) + ' 00:00:00'
        print (start_time, end_time)
        request = login_chrome_phone('ddk6049', 'ddk6049', start_time=start_time, end_time=end_time)
        gp = get_phone(request)
        gp.crawler_all()
        request.close_chrome()
        tomorrow = today + datetime.timedelta(days=1)
        d1 = datetime.datetime.strptime(str(tomorrow) + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
        cur = datetime.datetime.now()
        print '.......processed   '
        time.sleep((d1 - cur).seconds)
    except Exception as e:
        print traceback.format_exc()