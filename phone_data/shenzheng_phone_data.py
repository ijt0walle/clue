# coding=utf-8
import datetime
import sys
import time
import traceback

import pymysql
from lxml import etree

from shenzheng_chrome_login import login_chrome_phone


class get_phone:

    def __init__(self,request):
        self.request = request
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.db = pymysql.connect(
            host='121.43.168.132',
            port=3307,
            user='maxwell',
            password='ED81A84EC3B290A4EFA26122test',
            database='test',
            charset='utf8',
        )

    def get_html_new(self,search_url):
        html1 = self.request.excute_chrome_url(search_url)
        html = etree.HTML(html1)
        return html


    def first_crawler(self, html):
        list = []
        try:
            cnt = len(html.xpath('//*[@id="checkList"]/tbody/*'))
            #5,cnt
            for i in range(3,cnt):
                try:
                    excel_list = []
                    for j in range(2,7):
                        if j == 3:
                            excel_list.append(html.xpath('//*[@id="checkList"]/tbody/tr[%d]/td[%d]/text()' % (i, j))[0].replace('\n', ''))
                        elif j == 4:
                            excel_list.append(html.xpath('//*[@id="checkList"]/tbody/tr[%d]/td[%d]/a/text()' % (i, j))[0])
                        elif j == 6:
                            excel_list.append(html.xpath('//*[@id="checkList"]/tbody/tr[%d]/td[%d]/text()' % (i, j))[0].strip())
                        else:
                            excel_list.append(html.xpath('//*[@id="checkList"]/tbody/tr[%d]/td[%d]/text()' % (i, j))[0])
                    list.append(excel_list)
                except Exception as e :
                    pass

        except:
            pass
        return list

    def crawler_all(self):
        html = self.request.get_curr_html()
        html1 = etree.HTML(html)
        excel_list_all = []
        try:
            cnt_all = int(html1.xpath('//*[@id="main"]/div/div[3]/text()')[0].split(' ')[-4].split('/')[-1])

            excel_list_all = self.first_crawler(html1)
            self.shenzheng_phone(excel_list_all)
            #有改变
            for i in range(1,cnt_all):
                print i
                next_page_html = self.request.click_by_text('下一页')
                next_page_html = etree.HTML(next_page_html)
                excel_list_all = self.first_crawler(next_page_html)
                self.shenzheng_phone(excel_list_all)
        except:
            pass
        return excel_list_all

    def close_cur(self,cur):
        try:
            if cur is not None:
                cur.close()
        except Exception as e:
            pass

    def shenzheng_phone(self,list1):
        #像表中插入数据
        for list_mid in list1:
            try:
                sql = 'insert into shenzheng_phone (md5_id,holding_time,calling_number,called_number,call_duration,phone_state,cramling_time)' \
                      'values(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")  ON DUPLICATE KEY UPDATE holding_time="%s",calling_number="%s",called_number="%s",call_duration="%s",phone_state="%s",cramling_time="%s"' \
                      % (str(list_mid[0])+str(list_mid[1]),list_mid[0], list_mid[1], list_mid[2],list_mid[3],list_mid[4],datetime.datetime.now(),list_mid[0], list_mid[1], list_mid[2], list_mid[3], list_mid[4], datetime.datetime.now())
                print sql
                cur = self.db.cursor()
                cur.execute(sql)
                self.db.commit()
            except Exception as e:
                print(traceback.format_exc())
            finally:
                self.close_cur(cur)

    def __del__(self):
        self.db.close()



def test():
    while(True):
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        start_time = str(yesterday)+' 00:00:00'
        end_time = str(today)+' 00:00:00'
        request = login_chrome_phone('ddk6049','ddk6049',start_time=start_time,end_time=end_time)
        gp = get_phone(request)
        # final_list = gp.crawler_all()
        gp.crawler_all()
        # print len(final_list)
        request.close_chrome()
        tomorrow = today + datetime.timedelta(days=1)
        d1 = datetime.datetime.strptime(str(tomorrow)+' 00:00:00', '%Y-%m-%d %H:%M:%S')
        cur = datetime.datetime.now()
        time.sleep((d1 - cur).seconds)



if __name__ == '__main__':
    test()

