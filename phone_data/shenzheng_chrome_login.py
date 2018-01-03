# coding=utf-8
from __future__ import print_function
from __future__ import print_function
import random
import time
import sys
from lxml import etree
from selenium.webdriver.support.ui import Select
from selenium import webdriver

class login_chrome_phone:
    search_index_url = 'http://119.23.72.65/outbound/index.php/Public/login'
    sleep_time = 25
    count = 3
    warning_sleep_time = 1

    def set_sleep_time(self,sleep_time):
        self.sleep_time = sleep_time

    def __init__(self,user_name,password,start_time,end_time):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.user_name = user_name
        self.password = password
        self.start_time = start_time
        self.end_time = end_time
        #执行chromedriver
        self.dr = webdriver.Chrome("/Users/qizhouli/Documents/chromedriver")
        #登录的界面
        self.url = 'http://119.23.72.65/outbound/index.php/Public/login'
        #删除之前的cookies
        self.dr.delete_all_cookies()
        #得到这个url的地址
        self.dr.get(self.url)
        #执行那些cookies
        self.get_cookies()
        #执行要爬取的数据地址
        self.dr.execute_script('window.open("http://119.23.72.65/outbound/index.php/Call/index");')
        self.dr.switch_to.window(self.dr.window_handles[-1])
        # #要爬取的开始时间点
        # self.dr.execute_script("document.getElementById(\"stime\").value ='2017-11-01 00:00:00';")
        # #要爬取的终止时间点
        # self.dr.execute_script("document.getElementById(\"etime\").value ='2017-11-29 00:00:00';")
        self.dr.execute_script("document.getElementById(\"stime\").value ='"+start_time+"';")
        self.dr.execute_script("document.getElementById(\"etime\").value ='"+end_time+"';")

        Select(self.dr.find_elements_by_xpath('//select[@id="queryRange"]')[0]).select_by_value('2')
        self.dr.find_element_by_xpath('//input[@type="submit"]').click()

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Charset': 'utf-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
            'Connection': 'keep-alive'
        }

        # set custom headers
        # for key, value in headers.iteritems():
        #     webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value
        #
        # # another way to set custome header
        # webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent'] = \
        #     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
        # cookies = [{u'domain': u'.1688.com', u'name': u'_tmp_ck_0', u'value': u'"Us6kfQ%2FxEOMq9lhAtSelFmv8mznbShBBPr2RR8pIaaGLchk4XmAJZW2jrs8vaUuurfLuDckResTvRwwcuYeoxabRj7NVBN9UpqQvfFUTs0kaiPUpBa%2Fh3VE9YATmnGdeC3iiReTQez%2FGiepCVFL8heieT5B0y%2BbPx7F8hK4VbnmG8bzRhOaJNDCnTrL%2BHzNt8M1U9kLhw2wPKb2RTQ6lR8mK600ST6DoAG3dvUFRUzhbArkUsVrYNyKzsaKy3sj4v7ASwWWPgOviubFRqAtvgHCSjZGXDKHq93mHzSuNQVdCdGXZ9g2xPL3gJiExxoZmsN%2F5hGRKNLQPtW0CebpxHIwdzcGx6YhbgYj8M%2BfFXtBNL6YU3I5mvgZkUnEMAnXOrEtF4UXSgY2QaCpoWhqxRDlwZfJZWsMwRdtjZln6UI1g9KZHR3ZjkttgPsVVMU4oEXzqva%2FgSosNnuzVClFjz%2FiGAqncrJssmCeDhN6BHIxEnf%2BKAHQuu1d%2B1IqYGQGMm6KNmfKT0VE5rhUV6wRdOrSQjrw9OwBauHK%2FHemGzRM%2FErORex%2FIjA%3D%3D"', u'path': u'/', u'httponly': False, u'secure': False}, {u'domain': u'.1688.com', u'name': u'isg', u'expires': u'\u5468\u4e00, 26 2\u6708 2018 11:00:22 GMT', u'value': u'AlZW_TCNE4eGbScjapynvRKlqwpY95ox0Ib-38C_QjnUg_YdKIfqQbzxyyWQ', u'expiry': 1519642822, u'path': u'/', u'httponly': False, u'secure': False}, {u'domain': u'.1688.com', u'name': u'ali_ab', u'expires': u'\u5468\u516d, 28 8\u6708 2027 11:00:23 GMT', u'value': u'116.231.50.80.1504090823466.0', u'expiry': 1819450823, u'path': u'/', u'httponly': False, u'secure': False}, {u'domain': u'.1688.com', u'name': u'__rn_alert__', u'expires': u'\u5468\u4e09, 30 8\u6708 2017 13:00:23 GMT', u'value': u'false', u'expiry': 1504098023, u'path': u'/', u'httponly': False, u'secure': False}, {u'domain': u'.1688.com', u'name': u'_show_user_unbind_div_', u'expires': u'\u5468\u4e09, 30 8\u6708 2017 13:00:23 GMT', u'value': u'b2b-33847824257114b_false', u'expiry': 1504098023, u'path': u'/', u'httponly': False, u'secure': False}, {u'domain': u'.1688.com', u'name': u'_show_sys_unbind_div_', u'expires': u'\u5468\u4e09, 30 8\u6708 2017 13:00:23 GMT', u'value': u'b2b-33847824257114b_false', u'expiry': 1504098023, u'path': u'/', u'httponly': False, u'secure': False}, {u'domain': u'.1688.com', u'name': u'_show_force_unbind_div_', u'expires': u'\u5468\u4e09, 30 8\u6708 2017 13:00:23 GMT', u'value': u'b2b-33847824257114b_false', u'expiry': 1504098023, u'path': u'/', u'httponly': False, u'secure': False}, {u'domain': u'.1688.com', u'name': u'_is_show_loginId_change_block_', u'expires': u'\u5468\u4e09, 30 8\u6708 2017 13:00:22 GMT', u'value': u'b2b-33847824257114b_false', u'expiry': 1504098022, u'path': u'/', u'httponly': False, u'secure': False}, {u'domain': u'.1688.com', u'name': u'_nk_', u'value': u'jWReyNHZ0aDcg5sJxm1jOQ%3D%3D', u'path': u'/', u'httponly': False, u'secure': False}, {u'domain': u'.1688.com', u'name': u'userIDNum', u'value': u'UarHITWxPOpPRROfEcBM2w%3D%3D', u'path': u'/', u'httponly': False, u'secure': False}, {u'domain': u'work.1688.com', u'name': u'CNZZDATA1253645563', u'expires': u'\u5468\u4e09, 28 2\u6708 2018 11:00:20 GMT', u'value': u'331431613-1504086350-%7C1504086350', u'expiry': 1519815620, u'path': u'/', u'httponly': False, u'secure': False}, {u'domain': u'.1688.com', u'name': u'UM_distinctid', u'expires': u'\u5468\u4e09, 28 2\u6708 2018 11:00:20 GMT', u'value': u'15e32cc914aa4e-0d209db3b-3d710557-c0000-15e32cc914b1ce', u'expiry': 1519815620, u'path': u'/', u'httponly': False, u'secure': False}, {u'domain': u'.1688.com', u'name': u'cna', u'expires': u'\u5468\u516d, 28 8\u6708 2027 11:00:20 GMT', u'value': u'sogtEs0JanwCAWVRSIcgBJzt', u'expiry': 1819450820, u'path': u'/', u'httponly': False, u'secure': False}, {u'domain': u'.work.1688.com', u'name': u'landingPage', u'expires': u'\u5468\u56db, 31 8\u6708 2017 11:00:21 GMT', u'value': u'home', u'expiry': 1504177221, u'path': u'/', u'httponly': False, u'secure': False}, {u'domain': u'.1688.com', u'name': u'_csrf_token', u'value': u'1504090821188', u'path': u'/', u'httponly': False, u'secure': False}, {u'domain': u'.1688.com', u'name': u'login', u'value': u'"kFeyVBJLQQI%3D"', u'path': u'/', u'httponly': False, u'secure': False}, {u'domain': u'.1688.com', u'name': u'__last_loginid__', u'expires': u'\u5468\u56db, 30 8\u6708 2018 11:00:21 GMT', u'value': u'bigbigboat211', u'expiry': 1535626821, u'path': u'/', u'httponly': False, u'secure': False}, {u'domain': u'.1688.com', u'name': u'unb', u'value': u'3384782425', u'path': u'/', u'httponly': True, u'secure': False}, {u'domain': u'.1688.com', u'name': u'last_mid', u'expires': u'\u5468\u56db, 30 8\u6708 2018 11:00:21 GMT', u'value': u'b2b-33847824257114b', u'expiry': 1535626821, u'path': u'/', u'httponly': False, u'secure': False}, {u'domain': u'.1688.com', u'name': u'userID', u'value': u'"Msniix6jVnZxQHXN8nG07sOawn3tOWGcy4ULOvjgKZs6sOlEpJKl9g%3D%3D"', u'path': u'/', u'httponly': False, u'secure': False}, {u'domain': u'.1688.com', u'name': u'LoginUmid', u'value': u'"5ZpCLQ3e2tLbWJcO1HCnhL%2BWgC4oJa8QK%2BqJuE45mdRTAhztWl1ziA%3D%3D"', u'path': u'/', u'httponly': False, u'secure': False}, {u'domain': u'.1688.com', u'name': u'tbsnid', u'value': u'NaLC%2FReNzlFlLdei4kucBwPZ64tSCpDCnIE7iWaJDPA6sOlEpJKl9g%3D%3D', u'path': u'/', u'httponly': True, u'secure': False}, {u'domain': u'.1688.com', u'name': u'_cn_slid_', u'expires': u'\u5468\u56db, 30 8\u6708 2018 11:00:20 GMT', u'value': u'"gmQwZB7%2F5s"', u'expiry': 1535626820, u'path': u'/', u'httponly': False, u'secure': False}, {u'domain': u'.1688.com', u'name': u'cn_tmp', u'value': u'"Z28mC+GqtZ3iqYC9nr53wDX5nzG9aojsR6zg8x0QEmNFb80Bvk9OloKdGBOR4AXIZI3msIR4KPCBXv5WoBs/m4cAU1SYnP4MZIbK5UiM8ztH9D6qhBT4ds9KkQUmgQeMN5STtUT1NlcIjqWQdwpkg8NZ+3xZeNfS+2sSkThUf7sUKG8LXZM4ZGRW2qzbqoka9zcbr0XWylLb/Y7LoOzONh+eGQ06rv1HsdkOqhUv6qJHtIaAcdqw+V3CgXcOTPsDAU/XDyhFDG0="', u'path': u'/', u'httponly': True, u'secure': False}, {u'domain': u'.1688.com', u'name': u'ali_apache_tracktmp', u'value': u'"c_w_signed=Y"', u'path': u'/', u'httponly': False, u'secure': False}, {u'domain': u'.1688.com', u'name': u'ali_apache_track', u'expires': u'\u5468\u4e94, 30 10\u6708 2020 20:46:59 GMT', u'value': u'"c_ms=1|c_mt=3|c_mid=b2b-33847824257114b|c_lid=bigbigboat211"', u'expiry': 1604090819, u'path': u'/', u'httponly': False, u'secure': False}, {u'domain': u'.1688.com', u'name': u'__cn_logon_id__', u'value': u'bigbigboat211', u'path': u'/', u'httponly': False, u'secure': False}, {u'domain': u'.1688.com', u'name': u'__cn_logon__', u'value': u'true', u'path': u'/', u'httponly': False, u'secure': False}, {u'domain': u'.1688.com', u'name': u'sg', u'value': u'15d', u'path': u'/', u'httponly': False, u'secure': False}, {u'domain': u'.1688.com', u'name': u'_tb_token_', u'value': u'e35e01438737e', u'path': u'/', u'httponly': False, u'secure': False}, {u'domain': u'.1688.com', u'name': u't', u'value': u'6fa331bfdee25339d5d80a3f603ffa2d', u'path': u'/', u'httponly': False, u'secure': False}, {u'domain': u'.1688.com', u'name': u'uss', u'expires': u'\u5468\u4e94, 29 9\u6708 2017 11:00:21 GMT', u'value': u'UIY7U4r6se2NUwDlEKiH66ReAQvcgRWV2BrOYF6XmW8qFWLxyBykjhhYIg%3D%3D', u'expiry': 1506682821, u'path': u'/', u'httponly': False, u'secure': False}, {u'domain': u'.1688.com', u'name': u'cookie17', u'value': u'UNN104VsRvERkg%3D%3D', u'path': u'/', u'httponly': True, u'secure': False}, {u'domain': u'.1688.com', u'name': u'cookie2', u'value': u'183b1d42484d36813fb5bc6711964f9c', u'path': u'/', u'httponly': True, u'secure': False}, {u'domain': u'.1688.com', u'name': u'cookie1', u'value': u'UNiFr1LFdZbbKQmC%2F1BneIMVzfxsyBDmJGfMSJXCQLg%3D', u'path': u'/', u'httponly': True, u'secure': False}, {u'domain': u'.1688.com', u'name': u'JSESSIONID', u'value': u'9L78ohHi1-E6GYNWeHAFTDS2CP39-AonVmTQ-3a3U', u'path': u'/', u'httponly': False, u'secure': False}]
        # for cookie in cookies:
        #     try:
        #         self.dr.add_cookie(cookie)
        #     except Exception as e:
        #         pass
        #start_url = "https://detail.tmall.com/item.htm?id=540212526343"
        # PROXY = "121.43.173.22:12394"
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--proxy-server=%s' % PROXY)
        # self.dr = webdriver.Chrome(
        #     executable_path='/Users/zmj/Documents/chromedriver',
        #     chrome_options=chrome_options)
        # self.dr = webdriver.Chrome("C:\Users\Administrator\Downloads\chromedriver_win32\chromedriver.exe")
        # # self.dr.set_page_load_timeout(10)
        # # self.dr.set_script_timeout(10)
        #
        # # self.dr.delete_all_cookies()
        # # self.dr.set_window_size(1280, 2400)  # optionalwindowHandle='current'
        # self.url = 'http://119.23.72.65/outbound/index.php/Public/login'
        # self.dr.delete_all_cookies()
        # self.dr.get(self.url)
        # self.get_cookies()
        # self.dr.execute_script('window.open("http://119.23.72.65/outbound/index.php/Call/index");')
        # self.dr.switch_to.window(self.dr.window_handles[-1])
        # self.dr.execute_script("document.getElementById(\"stime\").value ='2017-11-01 00:00:00';")
        # self.dr.execute_script("document.getElementById(\"etime\").value ='2017-11-29 00:00:00';")
        # # self.dr.find_elements_by_xpath('//input[@class="input btn small"]')[0].
        # Select(self.dr.find_elements_by_xpath('//select[@id="queryRange"]')[0]).select_by_value('2')
        # self.dr.find_element_by_xpath('//input[@type="submit"]').click()

    def get_frame(self,text):
        self.dr.switch_to.frame(text)
        time.sleep(2)
        return self.dr.page_source

    def get_cookies(self):
        try:
            self.dr.get(self.url)
            time.sleep(1)
            # loginframe = self.dr.find_element_by_xpath('//*[@id="loginchina"]/iframe')
            # self.dr.switch_to.frame(loginframe)
            # print self.dr.page_source
            time.sleep(3)
            self.dr.find_element_by_id("username").clear()
            self.dr.find_element_by_id("password").clear()
            self.dr.find_element_by_id("username").send_keys(self.user_name)
            time.sleep(2)
            self.dr.find_element_by_id("password").send_keys(self.password)
            time.sleep(2)
            self.dr.find_element_by_xpath('//*[@id="TabbedPanels1"]/div/div/table/tbody/tr[4]/td/p/input[1]').click()
            time.sleep(3)
            #cookies = self.dr.get_cookies()
            #print("cookie = %s" % str(cookies))
            #print(self.dr.page_source)#
        except Exception as e:
            print(e)

    def click_by_contains_url(self, url):
        html = ''
        if url is None or len(str(url)) < 5:
            print(url + 'is not url')
            return html
        url = url.split('?')[0]
        index = 0
        html = ''
        while self.count >= index:
            try:
                click_element = self.dr.find_element_by_xpath("//a[contains(@href, '" + str(url) + "')]")
                html = self.excute_click(click_element)
                if html is None or len(html) < 10:
                    index += 1
                    time.sleep(3)
                else:
                    return self.dectected_click_status(html, click_element)
            except Exception as e:
                print(url)
                print(str(url) + " is not exists " + str(e))
                index += 1
                time.sleep(3)
        return html

    def click_by_text(self, text):
        html = ''
        index = 0
        while self.count >= index:
            try:
                click_element = self.dr.find_element_by_link_text(text)
                time.sleep(2)
                html = self.excute_click(click_element)
                if html is None or len(html) < 10:
                    index += 1
                    time.sleep(1)
                else:
                    return html
            except Exception as e:
                print(text)
                print(str(text) + " is not exists " + str(e))
                index += 1
                time.sleep(1)
        # self.dr.find_element_by_xpath()
        return html

    def get_curr_html(self):
        return self.dr.page_source

    def excute_click(self, url):
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

    def excute_url(self, url):
        html = ''
        try:
            all_handles = self.dr.window_handles
            window_size = len(all_handles)
            self.dr.get(url)
            time.sleep(self.get_time_sleep())
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

    def dectected_click_status(self, html, url):
        html_new = html
        while True:
            status = self.detected_status(html_new)
            if status > 0:
                #                self.dr.back()
                time.sleep(self.warning_sleep_time)
                html_new = self.excute_click(url)
            else:
                return html_new

    def element_click(self, url):
        self.dr.find_element_by_xpath(url).click()
        html = self.dr.page_source
        time.sleep(5)
        return html

    def detected_url_status(self, html, url):
        html_new = html
        while True:
            status = self.detected_status(html_new)
            if status > 0:
                # self.dr.back()
                time.sleep(self.warning_sleep_time)
                html_new = self.excute_url(url)
            else:
                return html_new

    def excute_chrome_url(self, url):
        try:
            html = self.excute_url(url)
            return self.detected_url_status(html, url)
        except Exception as e:
            print(e)

    # 诊断状态
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
                # time.sleep(3600)
                self.logger.error("302")
                return 302;
            else:
                return 0;
        except Exception as e:
            pass
        return 0

    # 时间延迟
    def get_time_sleep(self):
        return self.sleep_time + int(random.uniform(1, 5))

    # 设置睡眠时间
    def set_sleep_time(self, t):
        self.sleep_time = t

    # 获取title
    def get_page_title(self):
        return self.dr.title

    def delte_panthomjs(self):
        try:
            self.dr.quit()
        except Exception as e:
            pass

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

    def close_chrome(self):
        self.dr.quit()

