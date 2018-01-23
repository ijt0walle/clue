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
company_set = set()
fuck_index=1
def isExsits(shop_name):
    if shop_name in company_set:
        return True
    if len(tools.readFromDB('121.43.168.132','maxwell','ED81A84EC3B290A4EFA26122test','test',3307,
               'select * from test.51job_shop where shop_name=%s',(shop_name,)))>0:
        company_set.add(shop_name)
        return True
    else:
        return False

def saveShop(shop):
    print json.dumps(shop)
    tools.executeDB('121.43.168.132','maxwell','ED81A84EC3B290A4EFA26122test','test',3307,
                    'INSERT IGNORE INTO test.51job_shop (`index`,`company_name`,`shop_name`,`class`,`legal_person`,`address`,`city`,`ext`) '
                    'VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
                    (0,shop['company_name'],shop['shop_name'],shop['class'],'',shop['address'],shop['city'],shop['ext'])
                    )
