# encoding: utf-8

from selenium import webdriver
import time
import sys
import tools
from selenium.webdriver.common.action_chains import ActionChains
import traceback
import json

'''设置编码'''
reload(sys)
sys.setdefaultencoding('utf-8')

def isExsits(shop_name):
    if len(tools.readFromDB('121.43.168.132','maxwell','ED81A84EC3B290A4EFA26122test','test',3307,
               'select * from test.tmall_shop where shop_name=%s',(shop_name,)))>0:
        return True
    else:
        return False
#保存到数据库
def saveShop(shop):
    tools.executeDB('121.43.168.132','maxwell','ED81A84EC3B290A4EFA26122test','test',3307,
                    'INSERT IGNORE INTO test.tmall_shop (`index`,`company_name`,`shop_name`,`class`,`legal_person`,`address`,`city`,`ext`) '
                    'VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
                    (shop['index'],shop['company_name'],shop['shop_name'],shop['class'],shop['legal_person'],
                     shop['address'],shop['city'],json.dumps(shop['ext']))
                    )


#爬取相关的内容，比如'描述相符','服务态度'
def extract(dr,word):
    pack={}
    eles = dr.find_elements_by_xpath('//li[contains(text(),"'+word+'")]')
    if len(eles) > 0:
        try:
            pack['A'] = tools.floatOrDefault(eles[0].find_element_by_xpath('.//a/em').get_attribute('innerHTML').strip(),0.0)
            x=eles[0].find_element_by_xpath('.//a/span/i').get_attribute('innerHTML').strip()
            y=tools.floatOrDefault(eles[0].find_element_by_xpath('.//a/span/em').get_attribute('innerHTML').strip().replace('%',''),0.0)
            if x=='高于':
                pack['B'] =y
            else:
                pack['B'] = -y
        except Exception as e:
            print 'traceback.format_exc():\n%s' % traceback.format_exc()
    return pack

def extract_shop_time(dr):
    eles=dr.find_elements_by_xpath('//span[@class="tm-shop-age-num"]')
    if len(eles)>0:
        return tools.floatOrDefault(eles[0].get_attribute('innerHTML').strip(),0.0)
#获取店铺所在的城市地址
def extract_shop_city(dr):
    eles = dr.find_elements_by_xpath('//div[@class="extend"]/ul/li[@class="locus"]/div[@class="right"]')
    if len(eles) > 0:
        return eles[0].get_attribute('innerHTML').strip()

def extract_goods(dr):
    rt=[]
    for ele in dr.find_elements_by_xpath('//dd[@class="detail"]'):
        pack={}
        eles=ele.find_elements_by_xpath('.//a')
        if len(eles)>0:
            pack['title']=eles[0].get_attribute('innerHTML').strip()
        eles = ele.find_elements_by_xpath('.//span[@class="c-price"]')
        if len(eles) > 0:
            pack['price'] = tools.floatOrDefault(eles[0].get_attribute('innerHTML').strip(),0.0)
        eles = ele.find_elements_by_xpath('.//span[@class="sale-num"]')
        if len(eles) > 0:
            pack['sale_num'] = tools.floatOrDefault(eles[0].get_attribute('innerHTML').strip(),0.0)

        rt.append(pack)
        if len(rt)>=10:
            break
    return rt