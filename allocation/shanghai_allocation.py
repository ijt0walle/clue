# coding=utf-8
import traceback

import pymysql as MySQLdb
import sys
import json
import random
import time

from qichacha.main import get_company_info

'''设置编码'''
reload(sys)
sys.setdefaultencoding('utf-8')

industry_category = '化妆品'

max_time = 30
min_time = 20
def readFromDB(host,user,passwd,db,port,sql):
    conn = None
    cur = None
    info = None
    try:
        conn = MySQLdb.connect(host=host, user=user, passwd=passwd,db=db, charset='utf8', port=port)
        cur = conn.cursor()
        info = cur.fetchmany(cur.execute(sql))
    except:
        print traceback.format_exc()
    finally:
        cur.close()
        conn.close()
    return info

def insetFromDB(host,user,passwd,db,port,sqls):
    conn = None
    cur = None
    info = None
    try:
        conn = MySQLdb.connect(host=host, user=user, passwd=passwd,db=db, charset='utf8', port=port)
        cur = conn.cursor()
        cur.execute(sqls)
        conn.commit()
        cur.close()
    except:
        print traceback.format_exc()
    finally:
        conn.commit()
        conn.close()
    return info


def inset(sqls):
    if sqls is None or len(sqls) == 0:
        return
    return insetFromDB('121.43.168.132', 'maxwell', 'ED81A84EC3B290A4EFA26122test', 'test', 3307,sqls)

def get_sql_data(sql):
    return readFromDB('121.43.168.132', 'maxwell', 'ED81A84EC3B290A4EFA26122test', 'test', 3307,sql)

def get_industry_categories():
    sql = 'select class_3 from test.crm_config where class_1 = \'%s\'' % industry_category
    return get_sql_data(sql)




def get_clues():
    sql = "select company_name,1688_result,id from test.`1688_clue_new`  where classi_1 = '化妆品' and clue_status >= 3 and 1688_consume = 0"

    return  get_sql_data(sql)


def is_contains(classi,categories):
    if classi.find(industry_category)>=0:
        return 1
    classi = str(classi)
    if classi is None or len(classi) == 0:
        return 0
    for category in categories:
        if classi.find(category[0])>=0 or category[0].find(classi)>=0:
            return 1
    return 0

def process_clue():
    categories = get_industry_categories()
    clues = get_clues()
    list_company = []
    index = 1
    for clue in clues:
        try:
            result = json.loads(clue[1].replace('\n','').replace('\r','').replace('\\','').replace('"[','[').replace(']"',']'))
            try:
                main_d = result.get('main_d')
            except Exception as e:
                result = json.dumps(result, ensure_ascii=False, encoding='UTF-8').encode("utf-8").replace(
                    '"', '\\"')
            main_d = "".join(result.get('classifications'))+str(main_d)
            if main_d is None:
                main_d = "".join(result.get('classifications'))
            contain = is_contains(main_d,categories)
            if contain != 1:
                continue
            info = get_company_info(clue[0],index)
            if info is None or len(info) <= 0:
                continue
            print  json.dumps(info, ensure_ascii=False, encoding='UTF-8').encode("utf-8").replace('"', '\\"')
            result['成立时间'] = info.get('成立时间')
            result['邮箱'] = info.get('邮箱')
            result['地址'] = info.get('地址')
            result['电话'] = info.get('电话')
            result['法人'] = info.get('法人')
            result['注册资本'] = info.get('注册资本')
            print  json.dumps(result, ensure_ascii=False, encoding='UTF-8').encode("utf-8").replace('"', '\\"')
            convert_result = json.dumps(result, ensure_ascii=False, encoding='UTF-8').encode("utf-8").replace(
                '"', '\\"')
            sql = "update 1688_clue_new set 1688_result ='%s', 1688_consume = 1 where id=%d" % (convert_result,clue[2])
            inset(sql)
            index += 1
            time.sleep(random.uniform(1,10))
        except Exception as e:
            print clue[0],clue[1].replace('\n','').replace('\r',''),clue[2]
            print traceback.format_exc()



def get_json(result):
    dict = {}
    try:
        if result.get('agent') == 1:
            dict['是否招商'] = '需要'
        else:
            dict['是否招商'] = '未知'
    except:
        pass
    print result
    dict['重复采购率'] = result.get('重复采购率')
    dict['累计买家数'] = result.get('累计买家数')
    dict['联系人'] = result.get('contact_name')
    dict['电话'] = result.get('telphone')
    dict['手机'] = result.get('phone')
    dict['评级'] = result.get('credit_level')
    dict['公司简介'] = result.get('company_intro')
    dict['客单价'] = result.get('unit_price')
    dict['最大单价']= result.get('min_price')
    dict['最大单价'] = result.get('max_price')
    dict['阿里注册时长'] = result.get('bus_year')
    dict['公司名称'] = result.get('company')
    dict['旺旺号'] = result.get('wang_wang')
    dict['注册资本'] = result.get('registered_capital')
    dict['累计成交数'] = result.get('累计成交数')
    dict['地址'] = result.get('address')
    dict['商家类型'] = result.get('model')
    dict['商家员工'] = result.get('company_persons')
    dict['商品名称'] = result.get('goods_title')
    dict['商品简介'] = result.get('classifications')
    dict['同行平均成交数'] = result.get('trade_avg_cnt')
    dict['同行平均卖家数'] = result.get('trade_user_cnt')
    dict['同行平均重复采购率'] = result.get('repeat_avg_buy_ratio')
    dict['法人'] = result.get('法人')
    dict['成立时间'] = result.get('成立时间')
    return dict

def get_region(company_name,address):
    try:
        if company_name is not None and company_name.find('上海')>=0 :
            return 1
        if address is not None and address.find('上海')>=0:
            return 1
    except:
        return 0
    return 0

process_clue()