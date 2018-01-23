# coding=utf-8
import json
import sys
import traceback
from urllib import urlencode
from mysql_db import Mysql_db
from parse_html import parse_1688
from parse_yellow_page import parse_1688_yellow_page, is_yellow_page
from util import get_time

class flow:

    def __init__(self, request,region,all_classi,url_region):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.request = request
        self.url_region = url_region
        self.start_url = 'https://s.1688.com/company/company_search.htm?&' + str(self.url_region)
        self.classi_1 = None
        self.classi_2 = None
        self.region = region
        self.all_classi = all_classi
        self.index = 0

    def get_classi_count(self):
        '''
        如果关键分类跑，则想数据库中添加记录，开始跑
        如果分类词都有了，查找没有跑完的分类词，查找的条件，1。状态0 2。更新时间大约1小时
        '''
        my_sql = Mysql_db()
        sql_detail = "select classi from crm_config_detail where region = '%s'" % self.region
        sql = "select class_3,class_1,class_2 from crm_config where class_1 = '%s' and class_3 not in (%s)" % (
        self.all_classi, sql_detail)
        result = my_sql.get_sql_data(sql)
        if result is None or len(result) == 0:
            sql = "select id,classi,count from crm_config_detail where region = '%s' and status = 0 and TIMESTAMPDIFF(MINUTE,updated_at,'%s')>60 limit 1" % (self.region,get_time())
            result = my_sql.get_sql_data(sql)
            if result is not None and len(result) > 0:
                my_sql.update(
                    "update crm_config_detail set updated_at = '%s' where id = %d" % (get_time(), result[0][0]))
        else:
            sql = "insert into crm_config_detail(classi,source,region,updated_at,count,status) values('%s','1688','%s','%s',1,0)" % (
            result[0][0], self.region, get_time())
            id = my_sql.insert(sql)
            return (id, result[0][0], 1)
        if result is None or len(result) == 0:
            return result
        return result[0]

    def set_request(self, request):
        self.request = request

    def get_page_index(self, i):
        parameters = '&pageSize=30&offset=0&beginPage=%d' % i
        return parameters

    def get_search_url(self, company):
        kw = company.encode(encoding='gb2312')
        kw = urlencode({'keywords': kw})
        search_url = self.start_url + '&' + kw
        return search_url

    def get_page_size(self, html):
        dict = {}
        parse_html = parse_1688('', dict)
        page_size = parse_html.get_page_size(html)
        try:
            if int(page_size) <= 1:
                return 1
            else:
                return int(page_size)
        except Exception as e:
            print('page size is none')
        return 1

    def process_classi(self):
        flag = 0
        index_count = 0
        while index_count<1000 and flag == self.search_classi():
            index_count +=1

    def search_classi(self):
        try:
            classi_cnt = self.get_classi_count()
            if classi_cnt is None or len(classi_cnt) == 0:
                return 1
            classi = classi_cnt[1]
            index = classi_cnt[2]
            search_url = self.get_search_url(classi) + str(self.get_page_index(index))
            html = self.request.excute_chrome_url(search_url)
            page_size = self.get_page_size(html)
            self.search_classi_page(html, classi, page_size, index, classi_cnt[0])
        except Exception as e:
            print 'traceback.format_exc():\n%s' % traceback.format_exc()
        return 0

    def search_classi_page(self, html, classi, page_size, index, class_id):
        if page_size <= 0 or index > page_size:
            return
        err_count = 0
        for i in range(index, page_size+1):
            try:
                print(str(classi) + "---->" + str(i))
                parse_html = parse_1688(classi, {})
                list = parse_html.parse_list_search(html)
                self.get_mysql_db(list, classi)
                if list is not None and len(list)>1:
                    Mysql_db().update("update crm_config_detail set count = %d,updated_at ='%s' where id = %d" % (
                        i, get_time(), class_id))
                html = self.request.click_by_text('下一页')
            except Exception as e:
                print 'traceback.format_exc():\n%s' % traceback.format_exc()
                err_count += 1
        if err_count <= 2:
            Mysql_db().update("update crm_config_detail set status = %d,updated_at ='%s' where id = %d" % (
                1, get_time(), class_id))

    def get_mysql_db(self, list, classi):
        if list is None or len(list) <= 0:
            return
        for dict in list:
            try:

                company_name = dict.get("company").encode("utf-8")
                result = Mysql_db().get_from_company_name('1688_clue_new', company_name)
                if result is not None and len(result) > 2 and int(result[2]) > 0:
                    print(company_name + str(' is passed by db exists'))
                    continue
                print(company_name + str(' is processing ....'))
                html = self.request.click_by_contains_url(dict.get('url'))
                is_yellow = is_yellow_page(html)
                if is_yellow == 0:
                    self.get_1688_reslut(company_name, html, dict, classi, result)
                else:
                    self.get_yellow_page(company_name, html, dict, classi)
            except Exception as e:
                print 'traceback.format_exc():\n%s' % traceback.format_exc()
            finally:
                self.request.close()

    def get_1688_reslut(self, company_name, html, dict, classi, result):
        parse_html = parse_1688(company_name, dict)
        if parse_html.resultItem.get('url') is not None and len(parse_html.resultItem.get('url')) > 50:
            return
        parse_html.parse_company_captial(html)
        html = self.request.click_by_contains_url('creditdetail.htm')
        if len(str(html)) > 100:
            parse_html.parse_company_info(html)
        results = parse_html.resultItem
        if self.is_telephone(results.get('telphone')) == 0 and self.is_telephone(
                results.get('phone')) == 0 and self.is_telephone(results.get('contact_name')) == 0:
            html = self.request.click_by_contains_url('contactinfo.htm')
            parse_html.parse_contactinfo(html)
        results = parse_html.resultItem
        convert_result = json.dumps(results, ensure_ascii=False, encoding='UTF-8').encode("utf-8").replace("'",
                                                                                                           '"').replace(
            '\t', '').replace('\n', '').replace('\r', '').replace(' ', '').replace('"', '\\"')
        self.insert_update_db(result, results, company_name, convert_result, classi)

    def get_yellow_page(self, company_name, html, dict, classi):
        yellow_page = parse_1688_yellow_page(company_name, dict)
        yellow_page.get_yellow_page_info(html)
        tables_info = yellow_page.get_table(html)
        for dic in tables_info:
            yellow_page.get_table_info(self.request.element_click(tables_info[dic]), dic)
        results = yellow_page.resultItem
        convert_result = json.dumps(results, ensure_ascii=False, encoding='UTF-8').encode("utf-8").replace("'",
                                                                                                           '"').replace(
            '\t', '').replace('\n', '').replace('\r', '').replace(' ', '').replace('"', '\\"')
        sql = "insert into test.1688_clue_new(company_name,clue_status,updated_at,1688_result,main_classi,page_home_url,classi_1,classi_2) values('%s',%d,'%s','%s','%s','%s','%s','%s')" % (
            company_name, 2, get_time(), convert_result, classi, results.get('url'), self.classi_1, self.classi_2)
        Mysql_db().insert(sql)

    def insert_update_db(self, result, results, company_name, convert_result, classi):
        if result is not None and len(str(result)) > 2:
            if self.is_telephone(results.get('telphone')) > 0 or self.is_telephone(results.get('phone')) > 0:
                sql = 'update %s set clue_status = 3,1688_result = \"%s\", updated_at= \"%s\" where id=%d;' % (
                '1688_clue_new', convert_result, get_time(), int(result[0]))
            elif self.is_telephone(results.get('contact_name')) > 0:
                sql = 'update %s set clue_status = 1,1688_result = \"%s\", updated_at= \"%s\" where id=%d;' % (
                '1688_clue_new', convert_result, get_time(), int(result[0]))
            Mysql_db().update(sql)
        else:
            if self.is_telephone(results.get('telphone')) > 0 or self.is_telephone(results.get('phone')) > 0:
                Mysql_db().insert(
                    "insert into test.1688_clue_new(company_name,clue_status,updated_at,1688_result,main_classi,page_home_url,page_achivers_url,classi_1,classi_2) values('%s',%d,'%s','%s','%s','%s',\'\','%s','%s')" % (
                    company_name, 3, get_time(), convert_result, classi, results.get('url'), self.classi_1,
                    self.classi_2))
            elif self.is_telephone(results.get('contact_name')) > 0:
                Mysql_db().insert(
                    "insert into test.1688_clue_new(company_name,clue_status,updated_at,1688_result,main_classi,page_home_url,page_achivers_url,classi_1,classi_2) values('%s',%d,'%s','%s','%s','%s',\'\','%s','%s')" % (
                    company_name, 1, get_time(), convert_result, classi, results.get('url'), self.classi_1,
                    self.classi_2))

    @staticmethod
    def is_telephone(phone):
        if phone is not None and len(str(phone)) > 5:
            return 1
        return 0