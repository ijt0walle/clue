# coding=utf-8
import sys
import pymysql
from lxml import etree
from login_shunqi import login_sq
import urllib2
from urllib import urlencode
from selenium import webdriver
import datetime
import traceback

class flow_qs:
    db = pymysql.connect(
            host='121.43.168.132',
            port=3307,
            user='maxwell',
            password='ED81A84EC3B290A4EFA26122test',
            database='test',
            charset='utf8',
        )

    def __init__(self, request):
        classi = '点点客'
        self.start_url = 'http://b2b.11467.com/search'
        self.request = request
        self.classi = classi
        # self.dr = webdriver.Chrome("C:\Users\Administrator\Downloads\chromedriver_win32\chromedriver.exe")
        reload(sys)
        sys.setdefaultencoding('utf-8')


    def first_qs(self):
        html1 = self.request.get_curr_html()
        html = etree.HTML(html1)
        cnt = len(html.xpath('//*[@id="il"]/div[2]/div/ul/*'))
        list_one = []
        #得到所有图片所在的url
        list_url = html.xpath('//em/span/@style')
        for i in range(len(list_url)):
            #将url转换成规范的形式
            list_url[i] = 'http:'+list_url[i].split("('")[1].split("')")[0]
            #打开url，并将图片保存到指定的目录下面
            binary_data = urllib2.urlopen(list_url[i]).read()
            temp_file = open('D:\\photo_num\\'+list_url[i].split('phone/')[1], 'wb')
            temp_file.write(binary_data)
            temp_file.close()

        for i in range(1,cnt+1):
            list_mid =[]
            try:
                list_mid.append(html.xpath('//*[@id="il"]/div[2]/div/ul/li[%d]/div[1]/h4/a' % i)[0].text)
            except:
                pass
            try:
                list_mid.append(html.xpath('//*[@id="il"]/div[2]/div/ul/li[%d]/div[1]/div[1]' % i)[0].text)
            except:
                pass
            try:
                list_mid.append(html.xpath('//*[@id="il"]/div[2]/div/ul/li[%d]/div[1]/div[2]' % i)[0].text[4:])
            except:
                pass
            try:
                list_mid.append(html.xpath('//*[@id="il"]/div[2]/div/ul/li[%d]/div[1]/div[3]' % i)[0].text[5:])
            except:
                pass
            try:
                list_mid.append(html.xpath('//*[@id="il"]/div[2]/div/ul/li[%d]/div[2]/div[1]' % i)[0].text[5:])
            except:
                pass
            list_one.append(list_mid)
        return list_one

def test():
    request = login_sq('13127831752','123456')

    gp = flow_qs(request)
    list_test = gp.first_qs()
    print list_test