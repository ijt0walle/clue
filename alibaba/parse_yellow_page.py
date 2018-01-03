# coding=utf-8
from __future__ import print_function

import re
import traceback
from lxml import etree
import sys
from util import stringQ2B, process_str, is_chinese, uniform


class parse_1688_yellow_page:
    count = 5
    company = ''
    time_sleep = 2000

    def set_reslut_item(self,result_item):
        self.resultItem = result_item

    def __init__(self, kw,result_item):
        if result_item is not None:
            self.resultItem = result_item
        else:
            self.resultItem = {}
        self.company = kw
        reload(sys)
        sys.setdefaultencoding('utf-8')

    def parse_list_search(self,html1):
        list = []
        html = None
        try:
            html = etree.HTML(html1)
        except:
            return
        url = ''
        # 公司名称
        aa = html.xpath('//*[@id="sw_mod_searchlist"]/ul/*');
        for i in range(0,len(aa)):
            reslutItem = self.get_offer_info(html,i+1)
            list.append(reslutItem)
        return list

    def get_yellow_page_info(self,html1):
        try:
            html = etree.HTML(html1)
        except:
            return
        status = 2
        try:
            company_intro = html.xpath('//*[@id="site_content"]/div[1]/div/div[1]/div/div[2]/div[2]/span')[0].text
        except Exception as e:
            company_intro = html.xpath('//*[@id="site_content"]/div[1]/div/div/div/div[2]/div[2]/span/text()')
            pass
        if company_intro is None or len(str(company_intro)) < 5:
            print ('company_intro is has no scrape')
        else:
            self.resultItem['company_intro'] = company_intro
        try:
            company_hidder = html.xpath('//*[@id="site_content"]/div[1]/div/div[1]/div/div[2]/p')[0].text
            if company_hidder is None or str(company_hidder)< 5:
                company_hidder = html.xpath('//*[@id="site_content"]/div[1]/div/div/div/div[2]/p')[0].text
            self.resultItem['company_hidder'] = process_str(company_hidder)
            self.get_contract_name(self.resultItem['company_hidder'])
            self.resultItem['title'] = process_str(html.xpath('/html/head/title')[0].text)
        except:
            self.logger.error(str(self.company) + str(e.message) + ",company_hidder")
        try:
            self.resultItem['classifications'] = process_str("".join(html.xpath('//meta[@name="keywords"]/@content')))
        except:
            self.logger.error(str(self.company) + str(e.message) + ",classifications")
        return status

    def get_contract_name(self,text):
        text = str(text).replace(' ','').replace('-','')
        regex= re.compile(r'1\d{10}',re.IGNORECASE)
        self.resultItem['phone'] = re.findall(regex,text)
        regex = re.compile(r'0\d{9, 11}', re.IGNORECASE)
        self.resultItem['telphone'] = re.findall(regex, text)
        try:
            strs = text.split('联系人')
            if len(strs) < 2:
                return
            contact_name = strs[1].replace(' ','').replace('，','.').replace(',','.').replace('。','.')
            strs = contact_name.split('.')
            if len(strs)<2:
                return
            self.resultItem['contact_name'] = strs[0]
        except Exception as e:
            print (traceback.format_exc())

    def get_table(self,html1):
        try:
            html = etree.HTML(html1)
        except:
            return
        try:
            t = 'table:'
            tables = {}
            len_table = len(html.xpath('//*[@id="site_content"]/div[1]/div/div[2]/div/div[2]/div/div[1]/*'))
            for i in range(1,len_table+1):
                text = html.xpath('//*[@id="site_content"]/div[1]/div/div[2]/div/div[2]/div/div[1]/div['+str(i)+']/h2')[0].text
                tables[str(t+text)] = '//*[@id="site_content"]/div[1]/div/div[2]/div/div[2]/div/div[1]/div['+str(i)+']'
            return tables
        except Exception as e:
            print (e)

    def get_table_info(self,html1,table_names):
        try:
            html = etree.HTML(html1)
        except:
            return
        table_info = []
        for row in html.xpath('//tr[td]'):
            row_list = []
            for i in row.itertext():
                col =  i.replace('\n','').replace('\t','').replace(' ','').replace(',','').replace('\'','')
                if len(col) == 0:
                    continue
                row_list.append(col)
            table_info.append(''.join(row_list))
        self.resultItem[table_names] = '\n'.join(table_info)

def is_yellow_page(html1):
    try:
        html = etree.HTML(html1)
        yellow_img = html.xpath('//*[@id="masthead-v4"]/img')[0].get('src')
        if yellow_img == 'https://cbu01.alicdn.com/cms/upload/2015/161/992/2299161_353646508.jpg':
            return 1
    except Exception as e:
        pass
    return 0









