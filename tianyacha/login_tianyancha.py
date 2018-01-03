# coding=utf-8
from __future__ import print_function
from __future__ import print_function
import random
import time
import sys
from lxml import etree
from selenium import webdriver

class login_tianyancha:
    search_index_url = 'https://www.tianyancha.com/login'
    sleep_time = 25
    count = 3
    warning_sleep_time = 1

    def set_sleep_time(self,sleep_time):
        self.sleep_time = sleep_time

    def __init__(self,user_name,password):
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
        # 执行chromedriver
        self.dr = webdriver.Chrome("/Users/qizhouli/Documents/chromedriver")
        #登录界面网址
        self.url = 'https://www.tianyancha.com/login'
        self.dr.delete_all_cookies()
        self.dr.get(self.url)
        self.get_cookies()
        self.dr.get('https://www.tianyancha.com/search?key=fsdfs&checkFrom=searchBox')

    def get_cookies(self):
        try:
            self.dr.get(self.url)
            time.sleep(1)
            self.dr.find_element_by_xpath('//*[@id="web-content"]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/input').clear()
            self.dr.find_element_by_xpath('//*[@id="web-content"]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/input').clear()
            self.dr.find_element_by_xpath(
                '//*[@id="web-content"]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/input').send_keys(self.user_name)
            time.sleep(1)
            self.dr.find_element_by_xpath(
                '//*[@id="web-content"]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/input').send_keys(self.password)
            time.sleep(1)
            self.dr.find_element_by_xpath('//*[@id="web-content"]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[5]').click()
            time.sleep(1)

        except Exception as e:
            print(e)

    def click_search_company_name(self,company_name):
        self.dr.find_element_by_xpath('//*[@id="header-company-search"]').clear()
        self.dr.find_element_by_xpath('//*[@id="header-company-search"]').send_keys(str(company_name).decode())
        time.sleep(0.5)
        self.dr.find_element_by_xpath('//*[@id="web-header"]/div/div/div[1]/div[2]/div[2]/div[1]/div').click()
        time.sleep(2)
        return self.dr.page_source

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
                html = self.excute_click(click_element)
                if html is None or len(html) < 10:
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

    def excute_click(self, url):
        html = None
        all_handles = self.dr.window_handles
        window_size = len(all_handles)
        try:
            if url is not None and str(url).find('element') >= 0:
                js = "q=document.documentElement.scrollTop=" + str(url.location.get('y') - 100)
                self.dr.execute_script(js)
                time.sleep(0.2)
                js = "q=document.documentElement.scorllleft=" + str(url.location.get('x'))
                self.dr.execute_script(js)
                time.sleep(0.2)
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