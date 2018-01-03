# coding=utf-8
import sys
from lxml import etree
from login_tianyancha import login_tianyancha
import traceback
import time
import random
from qichacha import tools

class get_tianyancha:
    def __init__(self, request,page_num):
        self.start_url = 'http://www.tianyancha.com/search/'
        self.request = request
        self.page_num = page_num
        reload(sys)
        sys.setdefaultencoding('utf-8')

    def set_request(self,request):
        self.request = request

    def first_info(self,company):
        list_all = []
        # 得到加入关键词之后的url地址
        search_url = request.click_search_company_name(company)
        #返回url对应的html
        html = etree.HTML(search_url)
        cnt = len(html.xpath('//*[@id="web-content"]/div/div/div/div[1]/div[3]/*'))
        for i in range(1,cnt+1):
            list_one = {}
            tmp = ''
            try:
                tmp = tools.str_process(html.xpath('//*[@id="web-content"]/div/div/div/div[1]/div[3]/div[%d]/div[2]/div[2]/div[3]/div/span[3]/em' % i)[0].text).lower()
            except Exception as e: pass
            try:
                title = html.xpath(
                    '//*[@id="web-content"]/div/div/div/div[1]/div[3]/div[%d]/div[2]/div[1]/a/span'%i)
                title = str(title[0].xpath('string(.)'.decode('utf-8'))).replace('\r', '').replace('\n', '')
                title = tools.str_process(title)
                if company.find(title)<0 and title.find(company)<0 and tmp.find(company)<0 and company.find(tmp)<0:
                    continue
                list_one['company_name'] = title
            except Exception as e:
                print e
            try:
                reppresenter = html.xpath(
                    '//*[@id="web-content"]/div/div/div/div[1]/div[3]/div[%d]/div[2]/div[2]/div[1]/div[1]/a'%i)
                reppresenter = str(reppresenter[0].xpath('string(.)'.decode('utf-8'))).replace('\r', '').replace(
                    '\n', '')
                list_one['legal_person']=reppresenter
            except Exception as e:
                print e
            try:
                money = html.xpath(
                    '//*[@id="web-content"]/div/div/div/div[1]/div[3]/div[%d]/div[2]/div[2]/div[1]/div[2]/span'%i)
                money = str(money[0].xpath('string(.)'.decode('utf-8'))).replace('\r', '').replace('\n', '')
                list_one['registered_capital'] = money
            except Exception as e:
                pass
            try:
                telephone = html.xpath(
                    '//*[@id="web-content"]/div/div/div/div[1]/div[3]/div[%d]/div[2]/div[2]/div[2]/div/span[2]'%i)
                telephone = str(telephone[0].xpath('string(.)'.decode('utf-8'))).replace('\r', '').replace('\n', '')
                #result['telephone'] = telephone
                list_one['phone'] = telephone
            except Exception as e:
                pass
            list_one['mail'] = ' '
            list_one['ext'] = ' '
            list_one['address'] = ' '
            list_one['soruce'] = 'tianyancha'
            return list_one
        return {}


source = 'tianyancha'
index = 1
request = login_tianyancha('18817572258','xjh12345')
gp = get_tianyancha(request,1)
while True:
    if 0 == index % 100:
        request.quit_driver()
        request = login_tianyancha('18817572258','xjh12345')
        gp.set_request(request)
    try:
        pack = tools.get_companies(source)

        #all companies has been processed ,so ,waiting
        if pack is None or len(pack) == 0:
            time.sleep(600)
            continue

        for company_name in pack:
            company_name = company_name[0]
            info = gp.first_info(tools.str_process(company_name))
            tools.saveShop(info)
            tools.saveCompany(company_name,source)
            time.sleep(random.uniform(10,20))
        time.sleep(10)

    except Exception as e:
        print 'traceback.format_exc():\n%s' % traceback.format_exc()
        time.sleep(600)
    index += 1



