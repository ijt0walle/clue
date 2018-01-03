
# coding=utf-8
import base64
import random
import time
import sys
import traceback
import urllib
from urllib import quote
from PIL import Image
from lxml import etree
from selenium import webdriver
from selenium.webdriver import ActionChains

class login_chrome_1688:
    search_index_url = 'https://s.1688.com/company/company_search.htm'
    sleep_time = 15
    count = 3
    captch_time = 300
    warning_sleep_time = 1

    def set_sleep_time(self,sleep_time):
        self.sleep_time = sleep_time

    def __init__(self,user_name,password,i):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.user_name = user_name
        self.password = password
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Charset': 'utf-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
            'Connection': 'keep-alive'
        }
        self.headers = []
        #self.headers.append('user-agent="ozilla/5.0 (Linux; Android 5.0.2; vivo Y31 Build/LRX22G; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043613 Safari/537.36 MicroMessenger/6.5.19.1140 NetType/WIFI Language/zh_CN"')
        #self.headers.append('user-agent="ozilla/5.0 (Linux; Android 5.0.2; vivo Y31 Build/LRX22G; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043613 Safari/537.36 MicroMessenger/6.5.19.1140 NetType/WIFI Language/zh_CN"')
        self.headers.append('user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"')
        self.headers.append('user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"')
        self.headers.append('user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"')
        self.headers.append('user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Safari/604.1.38"')
        self.headers.append('user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) 			Chrome/55.0.2883.95 Safari/537.36"')
        self.headers.append('user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"')
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
        #chrome_options = webdriver.ChromeOptions()
        chrome_options = webdriver.ChromeOptions()
        # 设置中文
        chrome_options.add_argument('lang=zh_CN.UTF-8')
        # 更换头部
        chrome_options.add_argument(self.headers[i%len(self.headers)])
        #chrome_options.add_argument('--proxy-server=%s' % PROXY)
        # self.dr = webdriver.Chrome(
        #     executable_path='/Users/zmj/Documents/chromedriver',
        #     chrome_options=chrome_options)
        self.dr = webdriver.Chrome(
            executable_path='/Users/qizhouli/Documents/chromedriver',
            chrome_options=chrome_options)
        #self.dr = webdriver.Chrome("/Users/qizhouli/Documents/chromedriver")
        # self.dr.set_page_load_timeout(10)
        # # 设置10秒脚本超时时间
        # self.dr.set_script_timeout(10)

        # self.dr.delete_all_cookies()
        # self.dr.set_window_size(1280, 2400)  # optionalwindowHandle='current'
        self.url = 'https://login.1688.com/member/signin.htm'
        # self.dr.get(self.url)
        # self.dr.delete_all_cookies()
        #time.sleep(60)
        self.get_cookies()

    def get_cookies(self):
        try:
            self.dr.get(self.url)
            time.sleep(5)
            self.dr.delete_all_cookies()
            loginframe = self.dr.find_element_by_xpath('//*[@id="loginchina"]/iframe')
            self.dr.switch_to.frame(loginframe)
            # print self.dr.page_source
            time.sleep(3)
            self.dr.find_element_by_id("J_Quick2Static").click()
            # ActionChains(self.dr).move_to_element(self.dr.find_element_by_xpath('//input[@id="TPL_username_1"]')).perform()
            # i = 0
            # while i < 20:
            #     ActionChains(self.dr).move_by_offset(1, 1).perform()
            #     time.sleep(0.05)
            #     i += 1

            self.dr.find_element_by_id("TPL_username_1").clear()
            self.dr.find_element_by_id("TPL_password_1").clear()
            self.dr.find_element_by_id("TPL_username_1").send_keys(self.user_name)
            time.sleep(2)
            self.dr.find_element_by_id("TPL_password_1").send_keys(self.password)
            time.sleep(60)
            self.dr.find_element_by_id("J_SubmitStatic").click()
            #time.sleep(60)
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

    def dectected_click_status(self,html,url):
        self.close_window()
        status = self.detected_status(html)
        flag = 0
        while status > 0:
            flag = 1
            self.get_captch_img()
            html = self.dr.page_source
            status = self.detected_status(html)
        if flag != 0:
            time.sleep(self.captch_time)
        return html

    def close_window(self):
        time.sleep(0.5)
        elements = self.dr.find_elements_by_xpath('//*[@id="sufei-dialog-close"]')
        if elements is not None and len(elements)>0:
            for i in range(0,5):
                try:
                    elements[0].click()
                    break
                except:
                    time.sleep(2)
                    print 'fu chaung dianjie shibai'

    def element_click(self,url):
        self.dr.find_element_by_xpath(url).click()
        html = self.dr.page_source
        return self.dectected_click_status(html, url)
        return html
    #
    # def detected_url_status(self,html,url):
    #     html_new = html
    #     while True:
    #         status = self.detected_status(html_new)
    #         if status > 0:
    #             #self.dr.back()
    #             time.sleep(self.warning_sleep_time)
    #             html_new = self.excute_url(url)
    #         else:
    #             return html_new

    def excute_chrome_url(self,url):
        try:
            html = self.excute_url(url)
            return self.dectected_click_status(html,url)
        except Exception as e:
            print(e)

    def detected_status(self, html):
        status = self.is_301(html)
        if status > 0:
            time.sleep(30)
            return status
        status = self.is_captcha(html)
        if status > 0:
            #time.sleep(self.captch_time)
            return status
        status = self.is_404(html)
        if status > 0:
            time.sleep(10)
            return status
        return 0

    def get_captch_img(self):
        try:
            img_path = './image/'+str(int(random.uniform(1,1000)))+str(time.time())+'.jpg'
            self.dr.save_screenshot(img_path)
            time.sleep(1)
            c = self.dr.find_element_by_xpath('//*[@id="checkcodeImg"]')
            x = c.location.get('x')
            y = c.location.get('y')
            xx = x + c.size.get('width')
            yy = y + c.size.get('height')
            im = Image.open(img_path)
            im = im.crop((int(x), int(y), int(xx), int(yy)))
            im.save(img_path)
            time.sleep(1)
            f = open(img_path, 'rb')  # 二进制方式打开图文件
            ls_f = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
            f.close()
            text = urllib.urlopen('http://121.43.173.22:8070/taobao/captch?img='+str(quote(ls_f))).read()
            if text is None or len(text)==0:
                return 'fdss'
            else:
                text = str(text).replace('"','').replace(' ','').replace('\n','')
            self.dr.find_element_by_id("checkcodeInput").clear()
            self.dr.find_element_by_id("checkcodeInput").send_keys(text)
            time.sleep(random.uniform(1,2))
            self.dr.find_element_by_xpath('//*[@id="query"]/div[2]/input').click()
            time.sleep(0.5)
        except Exception as e:
            print (traceback.format_exc())
            time.sleep(300)
            
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
                return 404
            else:
                return 0;
        except Exception as e:
            pass
        return 0

    def is_captcha(self, html1):
        try:
            html = etree.HTML(html1)
            xpath = html.xpath('//*[@id="query"]/div[1]/p[3]/label')[0].text
            if xpath.find('验证码') >= 0:
                return 302;
            else:
                return 0;
        except Exception as e:
            pass
        return 0

    def get_time_sleep(self):
        return self.sleep_time+int(random.uniform(1, 5))

    def set_sleep_time(self, t):
        self.sleep_time = t

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

if __name__ == '__main__':
    request = login_chrome_1688('flesdewe234','lqz123456789')
    request.excute_phantomJS('http://www.baidu.com/')
    dict = [{u'\u91cd\u590d\u91c7\u8d2d\u7387:': '24.8%', 'main_d': u'\u6bdb\u5dfe;,\u65b9\u5dfe;,\u6d74\u5dfe;',
     'url': 'https://sanlitowel.1688.com', 'company': u'\u4e09\u5229\u96c6\u56e2\u670d\u9970\u6709\u9650\u516c\u53f8',
     'shop_name': u'\u90fd\u8c6a\u65d7\u8230\u5e97\uff5c', 'company_persons': u'16\u4eba',
     u'\u7d2f\u8ba1\u6210\u4ea4\u6570:': u'208\u7b14',
     'address': u' \u4e0a\u6d77\u5e02\u95f5\u884c\u533a \u8054\u822a\u8def1188...', 'model': u'\u8d38\u6613\u578b',
     u'\u81ea\u6709\u54c1\u724c:': u'\u96bd\u4f18,\u96bd\u4f18,COVATOR,COVATOR'}]

