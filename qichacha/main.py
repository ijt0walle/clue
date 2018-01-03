# encoding: utf-8

import sys
import time
import traceback

import datetime
from selenium import webdriver
from selenium.webdriver import ActionChains

import tools
from parse_qichacha import getShopInfo
import random
import json
import random

'''设置编码'''
reload(sys)
sys.setdefaultencoding('utf-8')

source = 'qichahca'
list_dr =[]
user_pds = tools.get_data("select user_name,pass_word from crm_clue_password where source = 'qichacha' limit 1")

def dragSlider(dr):
    w = dr.find_element_by_xpath('//*[@id="nc_1_wrapper"]')
    width1 = w.size.get("width")
    dragger = dr.find_element_by_xpath('//*[@id="nc_1_n1z"]')
    width2 = dragger.size.get("width")
    width = width1 - width2
    ActionChains(dr).move_to_element(dragger).perform()  # 将鼠标移动到这里
    ActionChains(dr).drag_and_drop_by_offset(dragger, width, 0).perform()  # 拖拽到指定位置

for user_pd in user_pds:
    print user_pd[0],user_pd[1]
    # 13501955864
    # 1234567890
    chrome_options = webdriver.ChromeOptions()
    # chrome_options('Cookie="_uab_collina=150279369017285020684195; _umdata=C234BF9D3AFA6FE752B758D28FB81D6DDDA04FC9577B1C5A91707F40241ED724B5C3925C86925A65CD43AD3E795C914CCFEA872821E84C9F0A90A3E18059D616; acw_tc=AQAAAKnBxxf1xwMAMsFgyidHB+teT71g; hasShow=1; PHPSESSID=nhkk49ss3ctla2np2al7l533s6; zg_did=%7B%22did%22%3A%20%2215de57bc4c7ccc-04c271b1ebe3b4-396b4c0b-1fa400-15de57bc4c89e0%22%7D; zg_3aa6aa556adf4e08a0542535203c5526=%7B%22sid%22%3A%201503391569175%2C%22updated%22%3A%201503391577396%2C%22info%22%3A%201502793680079%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.sogou.com%22%2C%22cuid%22%3A%20%2276e44d7ebb0c2ead91d0a5093f67487f%22%7D"')
    chrome_options.add_argument(
        'User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
    # PROXY = "121.43.189.255:84712394"
    # chrome_options.add_argument('--proxy-server=%s' % PROXY)
    # chrome_options.add_experimental_option("prefs",{"profile.managed_default_content_settings.images":2})
    dr = webdriver.Chrome(executable_path='/Users/qizhouli/Documents/chromedriver', chrome_options=chrome_options)
    dr.get('http://www.qichacha.com/user_login')
    try:
        time.sleep(1)
        dr.find_element_by_xpath('//*[@id="nameNormal"]').clear()
        dr.find_element_by_xpath('//*[@id="pwdNormal"]').clear()
        dr.find_element_by_xpath('//*[@id="nameNormal"]').send_keys(user_pd[0])
        time.sleep(1)
        dr.find_element_by_xpath('//*[@id="pwdNormal"]').send_keys(user_pd[1])
        time.sleep(1)
        dragSlider(dr)
        mistake = dr.find_element_by_xpath('//*[@id="dom_id_one"]/div/span/a')
        # if len(str(mistake)) > 0:
        #     dr.find_element_by_xpath('//*[@id="dom_id_one"]/div/span/a').click()
        #     dragSlider(dr)
    # dr.find_element_by_xpath('//input[@id="searchkey"]').send_keys("baidu")
    # dr.find_element_by_xpath('//input[@id="V3_Search_bt"]').click()
    except Exception as e:
        print(e)
    list_dr.append(dr)
    time.sleep(15)
    #dr.get('http://www.qichacha.com/search?key=ba')
'''begin'''
def get_chrome(dr_index):
    index = dr_index % len(list_dr)
    return list_dr[index]

def get_company_info(company_name,index):
    dr = get_chrome(index)
    company_data = tools.get_data("select company_name from crm_clue_qichacha where company_name = '%s'" % company_name)
    if company_data is not None and len(company_data) >0:
        tools.update_sql("update 1688_clue_new set 1688_consume =1 where company_name = '%s'" % company_name)
        print '%s is exists in db' % company_name
    else:
        infos = getShopInfo(dr, tools.str_process(company_name))
        insert_into_db(infos)

def insert_into_db(infos):
    for info in infos:
        try:
            company_name = info.get("公司名称")
            convert_result = json.dumps(info, ensure_ascii=False, encoding='UTF-8').encode("utf-8").replace('"', '\\"')
            time_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            tools.update_sql("insert into crm_clue_qichacha (company_name,status,result,created_at,updated_at) values('%s',1,'%s','%s','%s') ON DUPLICATE KEY UPDATE updated_at='%s'" % (company_name,convert_result,time_date,time_date,time_date))
            print convert_result
        except Exception as e:
            print 'traceback.format_exc():\n%s' % traceback.format_exc()


def from_1688_company():
    while True:
        index = 0
        chrome_len = len(list_dr)
        company_names = tools.get_data("select company_name,1688_result,id from test.`1688_clue_new` where 1688_consume = 0")
        for company_name in company_names:
            try:
                get_company_info(company_name[0],index % chrome_len)
                tools.update_sql("update 1688_clue_new set 1688_consume =1 where company_name = '%s'" % company_name[0])
                time.sleep(random.uniform(5,10))
                index += 1
            except:
                print 'traceback.format_exc():\n%s' % traceback.format_exc()
        time.sleep(3600)

from_1688_company()

