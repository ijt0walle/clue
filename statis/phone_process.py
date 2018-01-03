# coding=utf-8

"""
Created on Fri Nov 03 16:54:46 2017

@author: liqizhou
"""

import datetime
import pandas as pd
import pymysql
import re
import time

from sqlalchemy import create_engine

con_4 = 'mysql+mysqldb://data_mining:M510A987h973B6FBCE7D41396ct@172.17.0.4:11813/crm_excel?charset=utf8'
con_132 = 'mysql+mysqldb://maxwell:ED81A84EC3B290A4EFA26122test@121.43.168.132:3307/sale_phone?charset=utf8'

def updated_at(update_at):
    if update_at is None or len(str(update_at)) <= 5:
        return '2028-01-01 00:00:00'
    else:
        return update_at


def get_phone1(phone):
    try:
        if phone is None or len(str(phone).strip()) == 0:
            return 0
        phones = str(phone).split(',')
        for p in phones:
            if len(p.strip()) == 11:
                return p
    except Exception as e:
        print e
    return 0


def get_landline(phone):
    if phone is None or len(str(phone)) == 0:
        return 0
    phones = str(phone).split(',')
    try:
        for p in phones:
            if p.find('-') > 0:
                return p.replace('-', '').replace(' ', '').split('/')[0]
    except Exception as e:
        pass
    return 0


def get_landline_p(phone):
    if phone is None or len(str(phone)) == 0:
        return 0
    phones = str(phone).split(',')
    try:
        for p in phones:
            if p.find('-') > 0:
                p = p.split('-', 2)[1]
                return p.replace('-', '').replace(' ', '').split('/')[0]
    except Exception as e:
        pass
    return 0


def mobile_deal(p):
    if p > 0:
        # p=u'13316289688正确号码'
        try:
            p = p.decode('utf8')
        except:
            p = p

        p = p.lstrip(u'0').split(' ')
        for pp in p:
            for ppp in re.split('\D', pp):
                if len(ppp) >= 11:
                    return ppp[-11:]
                elif len(ppp) < 7:
                    continue
                else:
                    return ppp
    return 0


def convert_type(data):
    data.update_at = data.update_at.astype('datetime64')
    return data[(data.allocation_time <= data.ts_start_time) & (data.update_at >= data.ts_start_time)]


def get_phone(phone_sql):
    mysql_conn = create_engine(con_132)
    data_dialing = pd.read_sql(phone_sql, mysql_conn)
    del mysql_conn
    data_dialing['id_new'] = range(0, len(data_dialing))
    data_dialing['phone'] = map(lambda x: mobile_deal(x), data_dialing.ts_dialing)
    data_dialing['ts_duration'] = map(lambda z: sum(map(lambda x, y: int(x) * y, z.split(':'), (3600, 60, 1))),
                                      data_dialing.ts_duration)
    print 'call data ' + str(len(data_dialing))

    con_crm = create_engine(con_4)
    sql = '''
    SELECT
        clue_id,company,phone,current_conversion_code,sale_id,allocation_time,updated_time,backreason
    FROM
        crm_excel.clue_process_new
    WHERE
        system_flag = 1688 and (updated_time is null or updated_time>\'2000-010-01 00:00:00\')
    '''
    print sql
    data_clue = pd.read_sql(sql, con_crm)

    sql = 'select sale_id,name,sale_fleet_name,status as is_leave from crm_excel.clue_crm_fleet'
    data_staff = pd.read_sql(sql, con_crm)
    data_staff.sale_id = data_staff.sale_id.astype('int64')
    del con_crm

    data_clue['phone_re'] = map(lambda x: get_phone1(x), data_clue.phone)
    data_clue['landline_re'] = map(lambda x: get_landline(x), data_clue.phone)
    data_clue['landline'] = map(lambda x: get_landline_p(x), data_clue.phone)
    data_clue['update_at'] = map(lambda x: updated_at(x), data_clue.updated_time)

    data1 = pd.merge(data_clue[data_clue.phone_re > 0][
                         ['update_at', 'backreason', 'landline_re', 'company', 'landline', 'phone_re', 'clue_id',
                          'sale_id', 'allocation_time', 'current_conversion_code']], data_dialing, left_on='phone_re',
                     right_on='phone', how='inner')
    data1 = convert_type(data1)

    data2 = pd.merge(data_clue[data_clue.landline_re > 0][
                         ['landline_re', 'backreason', 'update_at', 'company', 'landline', 'phone_re', 'clue_id',
                          'sale_id', 'allocation_time', 'current_conversion_code']], data_dialing,
                     left_on='landline_re', right_on='phone',
                     how='inner')
    data2 = convert_type(data2)

    data3 = pd.merge(data_clue[data_clue.landline > 0][
                         ['update_at', 'backreason', 'landline_re', 'landline', 'company', 'phone_re', 'clue_id',
                          'sale_id', 'allocation_time', 'current_conversion_code']], data_dialing, left_on='landline',
                     right_on='phone',
                     how='inner')
    data3 = convert_type(data3)

    data = data1.append(data2).append(data3)
    data = data.drop_duplicates(['clue_id'])[['clue_id', 'ts_dialing', 'ts_start_time', 'ts_duration']]
    data1 = pd.merge(data_clue, data, left_on='clue_id', right_on='clue_id', how='left')
    data = pd.merge(data1, data_staff, left_on='sale_id', right_on='sale_id', how='left')
    data = data.drop_duplicates(['clue_id'])[
        ['clue_id', 'company', 'sale_id', 'name', 'sale_fleet_name', 'is_leave', 'phone_re', 'landline_re',
         'ts_dialing', 'backreason', 'allocation_time', 'ts_start_time', 'update_at', 'ts_duration',
         'current_conversion_code']]
    data['c_updated_at'] = datetime.datetime.now()
    data['s_num'] = 0
    data['act_num'] = 0
    data['cont_num'] = 0

    print ('data processed ......')


    con_crm = create_engine(con_4)

    data.to_sql('bigdata_phone_reslut_tmp', con_crm, index=False,if_exists='replace')

    del con_crm

    con_crm = pymysql.connect(host='172.17.0.4', port=11813, user='data_mining', passwd='M510A987h973B6FBCE7D41396ct',
                              charset='utf8', db='crm_excel')
    cursor = con_crm.cursor()

    cursor.execute('''INSERT INTO bigdata_phone_reslut SELECT * FROM bigdata_phone_reslut_tmp ON DUPLICATE KEY UPDATE
                        bigdata_phone_reslut.company =bigdata_phone_reslut_tmp.company,
                        bigdata_phone_reslut.sale_id =bigdata_phone_reslut_tmp.sale_id,
                        bigdata_phone_reslut.name =bigdata_phone_reslut_tmp.name,
                        bigdata_phone_reslut.sale_fleet_name =bigdata_phone_reslut_tmp.sale_fleet_name,
                        bigdata_phone_reslut.is_leave =bigdata_phone_reslut_tmp.is_leave,
                        bigdata_phone_reslut.phone_re =bigdata_phone_reslut_tmp.phone_re,
                        bigdata_phone_reslut.landline_re =bigdata_phone_reslut_tmp.landline_re,
                        bigdata_phone_reslut.ts_dialing =bigdata_phone_reslut_tmp.ts_dialing,
                        bigdata_phone_reslut.allocation_time =bigdata_phone_reslut_tmp.allocation_time,
                        bigdata_phone_reslut.ts_start_time =bigdata_phone_reslut_tmp.ts_start_time,
                        bigdata_phone_reslut.update_at =bigdata_phone_reslut_tmp.update_at,
                        bigdata_phone_reslut.ts_duration =bigdata_phone_reslut_tmp.ts_duration,
                        bigdata_phone_reslut.current_conversion_code =bigdata_phone_reslut_tmp.current_conversion_code,
                        bigdata_phone_reslut.backreason =bigdata_phone_reslut_tmp.backreason,
                        bigdata_phone_reslut.c_updated_at =bigdata_phone_reslut_tmp.c_updated_at''')
    con_crm.commit()
    del cursor

    print('writer to mysql ')

    cursor = con_crm.cursor()
    sql = '''
    select c.clue_id as clue_id,count(s.id) s_num,count(act.id) act_num,count(cont.id) cont_num
    from (select * from crm_excel.clue_process_new) c
    left join 
    (select id,bd_clue_id,stage from 
    weixin_crm.newcrm_saleschance
    where is_delete=1
    and cuid not in(SELECT id FROM weixin_crm.newcrm_staff
    where status=1
    and is_test=1))s
    on c.clue_id=s.bd_clue_id
    left join 
    (select id,from_id,type
    from weixin_crm.newcrm_activity
    where from_type=4
    and type=9
    and is_delete=1)act
    on act.from_id=s.id
    left join 
    (select id,saleschange_id,ht_status
    from weixin_crm.newcrm_contract
    where status=1
    and cuid not in(SELECT id FROM weixin_crm.newcrm_staff
    where status=1
    and is_test=1)) cont
    on cont.saleschange_id=s.id
    group by c.clue_id having s_num>0
    '''
    data_clue = pd.read_sql(sql, con_crm)

    for row in data_clue.iterrows():
        try:
            sql = 'insert into bigdata_phone_reslut (clue_id,s_num,act_num,cont_num) values(\'%s\',%d,%d,%d) on duplicate key update s_num = %d,act_num=%d,cont_num=%d' % (
                str(row[1].clue_id), int(row[1].s_num), int(row[1].act_num), int(row[1].cont_num), int(row[1].s_num),
                int(row[1].act_num), int(row[1].cont_num))
            cursor.execute(sql)
            con_crm.commit()
        except Exception as e:
            print e
    del cursor
    del con_crm


def get_sql():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=3)
    start_time = str(yesterday) + ' 00:00:00'
    end_time = str(today) + ' 00:00:00'
    sql = 'select ts_id,ts_line_number,ts_start_time,ts_dialing,ts_duration,fm_line from sale_phone.phone_dialing where ts_start_time>= \'%s\' and ts_start_time<\'%s\' ' \
          ' UNION ' \
          'select  1 as ts_id,calling_number as ts_line_number,cramling_time as ts_start_time,called_number as ts_dialing,call_duration as ts_duration,100  as fm_line from test.shenzheng_phone where cramling_time>= \'%s\'  and cramling_time<\'%s\' ' % (
              start_time, end_time, start_time, end_time)
    return sql


def main():
    while (True):
        try:
            sql = get_sql()
            get_phone(sql)
        except Exception as e:
            print e
        print('processed ...........')
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        d1 = datetime.datetime.strptime(str(tomorrow) + ' 05:00:00', '%Y-%m-%d %H:%M:%S')
        cur = datetime.datetime.now()
        time.sleep((d1 - cur).seconds)


main()
# sql = '''CREATE TABLE `bigdata_phone_reslut` (
#    `clue_id` varchar(63) DEFAULT NULL,
#    `company` varchar(63) DEFAULT NULL,
#    `sale_id` bigint(11) DEFAULT NULL,
#    `name` varchar(63) DEFAULT NULL,
#    `sale_fleet_name` varchar(63) DEFAULT NULL,
#    `is_leave` bigint(11) DEFAULT NULL,
#    `phone_re` varchar(63) DEFAULT NULL,
#    `landline_re` varchar(63) DEFAULT NULL,
#    `ts_dialing` varchar(63) DEFAULT NULL,
#    `backreason` varchar(63) DEFAULT NULL,
#    `allocation_time` datetime DEFAULT NULL,
#    `ts_start_time` datetime DEFAULT NULL,
#    `update_at` varchar(63) DEFAULT NULL,
#    `ts_duration` double DEFAULT NULL,
#    `current_conversion_code` varchar(63) DEFAULT NULL,
#    `c_updated_at` datetime DEFAULT NULL,
#    `s_num` bigint(11) DEFAULT NULL,
#    `act_num` bigint(1) DEFAULT NULL,
#    `cont_num` bigint(11) DEFAULT NULL
#    PRIMARY KEY (`clue_id`)
#  ) ENGINE=InnoDB DEFAULT CHARSET=utf8'''