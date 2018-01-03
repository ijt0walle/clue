# coding=utf-8
from __future__ import print_function
from __future__ import print_function
import random
import time
import sys
from lxml import etree

from selenium import webdriver
class login_qxbao:
    search_index_url = 'http://www.qixin.com/auth/login?return_url=%2F'
    sleep_time = 25
    count = 3
    warning_sleep_time = 1

    def get_cookie(self):
        self.dr.delete_all_cookies()
        self.dr.add_cookie({u'domain': u'www.qixin.com',
          u'expiry': 1514735999,
          u'httpOnly': False,
          u'name': u'showsale',
          u'path': u'/',
          u'secure': False,
          u'value': u'1'})
        self.dr.add_cookie({u'domain': u'.qixin.com',
          u'expiry': 1544594263,
          u'httpOnly': False,
          u'name': u'_zg',
          u'path': u'/',
          u'secure': False,
          u'value': u'%7B%22uuid%22%3A%20%22160494cc7e7560-01dfdbcc2c8766-17386d57-1fa400-160494cc7e84f5%22%2C%22sid%22%3A%201513058256.874%2C%22updated%22%3A%201513058263.618%2C%22info%22%3A%201513058256880%2C%22cuid%22%3A%20%22ed9054a4-c3fa-4299-bbdb-a32b27dd71e8%22%7D'})
        self.dr.add_cookie({u'domain': u'www.qixin.com',
          u'httpOnly': False,
          u'name': u'responseTimeline',
          u'path': u'/',
          u'secure': False,
          u'value': u'57'})
        self.dr.add_cookie({u'domain': u'.qixin.com',
          u'httpOnly': False,
          u'name': u'Hm_lpvt_52d64b8d3f6d42a2e416d59635df3f71',
          u'path': u'/',
          u'secure': False,
          u'value': u'1513058264'})
        self.dr.add_cookie({u'domain': u'www.qixin.com',
          u'httpOnly': True,
          u'name': u'sid',
          u'path': u'/',
          u'secure': False,
          u'value': u's%3AokHKvT86wIfCz2b9Xfd8fWHSUhplO4R1.ZminRXVLRno0RzMd4emL0coz9MJm0w4Ih01z0PkEuSs'})
        self.dr.add_cookie({u'domain': u'.qixin.com',
          u'expiry': 1544594263,
          u'httpOnly': False,
          u'name': u'Hm_lvt_52d64b8d3f6d42a2e416d59635df3f71',
          u'path': u'/',
          u'secure': False,
          u'value': u'1513058257'})
        self.dr.add_cookie({u'domain': u'www.qixin.com',
          u'httpOnly': True,
          u'name': u'aliyungf_tc',
          u'path': u'/',
          u'secure': False,
          u'value': u'AQAAAKPfLkvKXAQA++VRZXm8SFntbTZr'})


    def set_sleep_time(self,sleep_time):
        self.sleep_time = sleep_time

    def __init__(self,user_name,password):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.user_name = user_name
        self.password = password

        self.headers = []
        self.headers.append(
            'user-agent="ozilla/5.0 (Linux; Android 5.0.2; vivo Y31 Build/LRX22G; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043613 Safari/537.36 MicroMessenger/6.5.19.1140 NetType/WIFI Language/zh_CN"')
        self.headers.append(
            'user-agent="ozilla/5.0 (Linux; Android 5.0.2; vivo Y31 Build/LRX22G; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043613 Safari/537.36 MicroMessenger/6.5.19.1140 NetType/WIFI Language/zh_CN"')
        self.headers.append(
            'user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"')
        self.headers.append(
            'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"')
        self.headers.append(
            'user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"')
        self.headers.append(
            'user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Safari/604.1.38"')
        self.headers.append(
            'user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) 			Chrome/55.0.2883.95 Safari/537.36"')
        self.headers.append(
            'user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"')
        chrome_options = webdriver.ChromeOptions()
        # 设置中文
        chrome_options.add_argument('lang=zh_CN.UTF-8')
        # 更换头部
        chrome_options.add_argument(self.headers[1])
        # chrome_options.add_argument('--proxy-server=%s' % PROXY)
        # self.dr = webdriver.Chrome(
        #     executable_path='/Users/zmj/Documents/chromedriver',
        #     chrome_options=chrome_options)
        self.dr = webdriver.Chrome(
            executable_path='/Users/qizhouli/Documents/chromedriver',
            chrome_options=chrome_options)
        # self.dr.set_page_load_timeout(10)
        # # 设置10秒脚本超时时间
        # self.dr.set_script_timeout(10)

        # self.dr.delete_all_cookies()
        # self.dr.set_window_size(1280, 2400)  # optionalwindowHandle='current'
        #登录界面的网址
        self.url = 'http://www.qixin.com/auth/login?return_url=%2F'
        self.dr.delete_all_cookies()
        self.dr.get(self.url)
        self.get_cookie()

    def get_cookies(self):
        try:
            self.dr.get(self.url)
            time.sleep(1)
            self.dr.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div/div/div/div/div[1]/input").clear()
            self.dr.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div/div/div/div/div[2]/input").clear()
            self.dr.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div/div/div/div/div[1]/input").send_keys(self.user_name)
            time.sleep(1)
            self.dr.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div/div/div/div/div[2]/input").send_keys(self.password)
            time.sleep(1)
            self.dr.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div/div/div/div/div[4]/a").click()
            time.sleep(1)
            #cookies = self.dr.get_cookies()
            #print("cookie = %s" % str(cookies))
            #print(self.dr.page_source)#
        except Exception as e:
            print(e)

    def click_by_contains_url(self,url):
        html = ''
        if url is None or len(str(url))<5:
            print(url + 'is not url')
            return html
        url = url.split('?')[0]
        index = 0
        html = ''
        while self.count >= index:
            try:
                click_element = self.dr.find_element_by_xpath("//a[contains(@href, '" + str(url) + "')]")
                html = self.excute_click(click_element)
                if html is None or len(html)<10:
                    index += 1
                    time.sleep(3)
                else:
                    return self.dectected_click_status(html,click_element)
            except Exception as e:
                print(url)
                print(str(url) + " is not exists " + str(e))
                index += 1
                time.sleep(3)
        return html

    def click_by_text(self,text):
        html = ''
        index = 0
        while self.count >= index:
            try:
                click_element = self.dr.find_element_by_link_text(text)
                html = self.excute_click(click_element)
                if html is None or len(html)<10:
                    index += 1
                    time.sleep(3)
                else:
                    return self.dectected_click_status(html, click_element)
            except Exception as e:
                print(text)
                print(str(text) + " is not exists " + str(e))
                index += 1
                time.sleep(3)
        return html

    def excute_click(self,url):
        html = None
        all_handles = self.dr.window_handles
        window_size = len(all_handles)
        try:
            if url is not None and str(url).find('element') >= 0:
                js = "q=document.documentElement.scrollTop=" + str(url.location.get('y') - 100)
                self.dr.execute_script(js)
                time.sleep(0.5)
                js = "q=document.documentElement.scorllleft=" + str(url.location.get('x'))
                self.dr.execute_script(js)
                time.sleep(0.5)
                url.click()
                time.sleep(self.get_time_sleep())
                all_handles = self.dr.window_handles
                new_window_size = len(all_handles)
                if new_window_size > window_size:
                    self.dr.switch_to_window(all_handles[len(all_handles) - 1])
                html = self.dr.page_source
            else:
                print(url + str('is not exists'))
        except Exception as e:
            print(str(url) + " is not exists " + str(e))
        return html

    def click_search_company_name(self,company_name):
        try:
            # self.dr.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/div/div/span/input[2]').clear()
            # self.dr.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/div/div/span/input[2]').send_keys(str(company_name).decode())
            # time.sleep(0.5)
            # self.dr.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/div/div/i').click()
            time.sleep(1)
        except Exception as e:
            print(e)
        return self.excute_url('http://www.qixin.com/search?key='+company_name+'&page=1')
        return self.dr.page_source

    def excute_url(self, url):
        html = ''
        try:
            all_handles = self.dr.window_handles
            window_size = len(all_handles)
            self.dr.get(url)
            #time.sleep(self.get_time_sleep())
            js = "var q=document.documentElement.scrollTop=100000"
            self.dr.execute_script(js)
            all_handles = self.dr.window_handles
            new_window_size = len(all_handles)
            if new_window_size > window_size:
                self.dr.switch_to_window(all_handles[len(all_handles) - 1])
            html = self.dr.page_source
        except Exception as e:
            print(e)
        return html

    def dectected_click_status(self,html,url):
        html_new = html
        while True:
            status = self.detected_status(html_new)
            if status > 0:
#                self.dr.back()
                time.sleep(self.warning_sleep_time)
                html_new = self.excute_click(url)
            else:
                return html_new
    def element_click(self,url):
        self.dr.find_element_by_xpath(url).click()
        html = self.dr.page_source
        time.sleep(5)
        return html

    def detected_url_status(self,html,url):
        html_new = html
        while True:
            status = self.detected_status(html_new)
            if status > 0:
                #self.dr.back()
                time.sleep(self.warning_sleep_time)
                html_new = self.excute_url(url)
            else:
                return html_new

    def excute_chrome_url(self,url):
        try:
            html = self.excute_url(url)
            return self.detected_url_status(html,url)
        except Exception as e:
            print(e)
    #诊断状态
    def detected_status(self, html):
        status = self.is_301(html)
        if status > 0:
            return status
        status = self.is_captcha(html)
        if status > 0:

            return status
        status = self.is_404(html)
        if status > 0:
            return status
        return 0

    def is_301(self, html):
        try:
            xpath = html.xpath('//*[@id="msgTip"]')[0].text
            if xpath.find('登录') >= 0:
                self.logger.error("302")
                return 301;
            else:
                return 0;
        except Exception as e:
            pass
        return 0;

    def is_404(self, html):
        try:
            xpath = html.xpath('//*[@id="msgTip"]')[0].text
            if xpath.find('登录') >= 0:
                self.logger.error("302")
                return 404;
            else:
                return 0;
        except Exception as e:
            pass
        return 0;

    def is_captcha(self, html1):
        try:
            html = etree.HTML(html1)
            xpath = html.xpath('//*[@id="query"]/div[1]/p[3]/label')[0].text
            if xpath.find('验证码') >= 0:
                #time.sleep(3600)
                self.logger.error("302")
                return 302;
            else:
                return 0;
        except Exception as e:
            pass
        return 0
    #时间延迟
    def get_time_sleep(self):
        return self.sleep_time+int(random.uniform(1, 5))
    #设置睡眠时间
    def set_sleep_time(self, t):
        self.sleep_time = t
    #获取title
    def get_page_title(self):
        return self.dr.title

    def delte_panthomjs(self):
        try:
            self.dr.quit()
        except Exception as e:
            pass

    def quit_driver(self):
        self.dr.quit()

    def close(self):
        while True:
            all_handles = self.dr.window_handles
            window_size = len(all_handles)
            if window_size > 1:
                self.dr.close()
                time.sleep(1)
                all_handles = self.dr.window_handles
                window_size = len(all_handles)
                self.dr.switch_to_window(all_handles[window_size - 1])
            else:
                self.dr.switch_to_window(all_handles[window_size - 1])
                return
