# coding=utf-8
import random
import sys
import traceback
import time
from lxml import etree
from login_q import login_qxbao
from qichacha import tools

source = 'qixinbao'
class get_qxbao:

    def __init__(self,request,page_num):
        self.start_url = 'http://www.qixin.com/search'
        self.request = request
        self.page_num = 1
        reload(sys)
        sys.setdefaultencoding('utf-8')

    def first_info(self,company):
        global mail, c_mail
        search_url = request.click_search_company_name(company_name)
        # 返回url对应的html
        html = etree.HTML(search_url)
        cnt = len(html.xpath('/html/body/div[5]/div/div[1]/div[3]/div[2]/*'))
        list_one = {}
        for i in range(1,cnt+1):
            try:
                title = (html.xpath('/html/body/div[5]/div/div[1]/div[3]/div[2]/div[%d]/div[2]/div[1]/div[1]' % i)[0].xpath('string(.)'.decode('utf-8')))
                list_one['company_name'] = title
                c = html.xpath('/html/body/div[5]/div/div[1]/div[3]/div[2]/div[%d]/div[2]/div[1]/div[5]/span' % i)[0].xpath('string(.)'.decode('utf-8'))
            except:
                c = ' '
            try:
                mail = (html.xpath('/html/body/div[5]/div/div[1]/div[3]/div[2]/div[%d]/div[2]/div[1]/div[3]/span[2]/a' % i)[0].xpath('string(.)'))
                list_one['mail'] = mail
            except:
                pass
            try:
                c_mail = str(mail).split('@')[1]
            except Exception as e:
                c_mail = ' '
            if company.find(title) < 0 and title.find(company) < 0 and c.find(company) < 0 and company.find(c) < 0 and c_mail.find(company) < 0  and company.find(c_mail)<0:
                continue
            try:
                list_one['legal_person']=(html.xpath('/html/body/div[5]/div/div[1]/div[3]/div[2]/div[%d]/div[2]/div[1]/div[2]' % i)[0].xpath('string(.)')[6:])
            except:
                pass
            try:
                list_one['phone'] = (html.xpath('/html/body/div[5]/div/div[1]/div[3]/div[2]/div[%d]/div[2]/div[1]/div[3]/span[1]/text()' % i)[0][3:])
            except:
                pass
            try:
                list_one['address'] = (html.xpath('/html/body/div[5]/div/div[1]/div[3]/div[2]/div[%d]/div[2]/div[1]/div[4]/span/text()' % i)[0][4:])
            except:
                pass
            try:
                list_one['registered_capital'] = (html.xpath('/html/body/div[5]/div/div[1]/div[3]/div[2]/div[%d]/div[3]/div[1]' % i)[0].xpath('string(.)'))
            except:
                pass
            try:
                list_one['ext'] = 'registered_time :'+(html.xpath('/html/body/div[5]/div/div[1]/div[3]/div[2]/div[%d]/div[3]/div[2]' % i)[0].xpath('string(.)'))
            except:
                pass
            list_one['soruce'] = source
        return list_one

index = 1
request = login_qxbao('13816320135','lqz356166493')
request.excute_chrome_url('http://www.qixin.com/search?key=JHKHK&page=1')
gp = get_qxbao(request,page_num=1)
while True:
    if 0 == index % 100:
        request.quit_driver()
        request = login_qxbao('18817572258', 'xjh12345')
        request.excute_chrome_url('http://www.qixin.com/search?key=JHKHK&page=1')
        gp = get_qxbao(request, page_num=1)
    try:
        pack = tools.get_companies(source)
        #all companies has been processed ,so ,waiting
        if pack is None or len(pack) == 0:
            print 'waiting ......'
            time.sleep(600)
            continue

        for company_name in pack:
            company_name = company_name[0]
            print company_name
            info = gp.first_info(tools.str_process(company_name))
            print info
            tools.saveShop(info)
            tools.saveCompany(company_name,source)
            time.sleep(random.uniform(10,20))
        time.sleep(6)

    except Exception as e:
        print 'traceback.format_exc():\n%s' % traceback.format_exc()
        time.sleep(600)
    finally:
        index += 1






