# encoding: utf-8

from selenium import webdriver
import time
import sys
import shop
import tools
from selenium.webdriver.common.action_chains import ActionChains
import traceback

'''设置编码'''
reload(sys)
sys.setdefaultencoding('utf-8')


main_dir='D:\\wjm\\51job'
PAGE=main_dir+'\\page'
SKIP=main_dir+'\\skip'
word=''
city=''
user=''
password=''
current_page=''
skip_words=set();

file_obj=open(PAGE)
for line in file_obj.readlines():
    current_page=line
file_obj.close()

file_obj=open(SKIP)
for line in file_obj.readlines():
    skip_words.add(unicode(line.strip(), 'utf-8'))
file_obj.close()

'''begin'''
chrome_options = webdriver.ChromeOptions()
dr = webdriver.Chrome(executable_path='D:\wjm\drivers\chromedriver.exe',chrome_options=chrome_options)
dr.get('http://search.51job.com')
city=dr.find_element_by_xpath('//span[@id="work_position_span"]').get_attribute('innerHTML')

def read(url):
    dr.get(url)
    tools.scrollToEnd(dr)
    classx=dr.find_element_by_xpath('//div[@class="dw_choice"]/div[@class="in"]/p').text
    while True:
        for company in dr.find_elements_by_xpath('//div[@id="resultList"]/div[@class="el"]/span/a'):
            company_a=company.get_attribute('title')
            if shop.isExsits(company_a):
                continue
            print company.get_attribute('outerHTML')
            dr.execute_script('window.open("'+company.get_attribute('href')+'");')
            dr.switch_to.window(dr.window_handles[-1])
            company={'company_name':'','shop_name':'','class':classx,'address':'','city':city,'ext':''}

            eles=dr.find_elements_by_xpath('//div[@class="con_msg"]/div[@class="in"]/p')
            if len(eles)>0:
                company['ext']=eles[0].text.strip()

            eles = dr.find_elements_by_xpath('//h1')
            if len(eles) > 0:
                company['company_name'] = eles[0].text.strip()
                company['shop_name'] = company['company_name']

            eles = dr.find_elements_by_xpath('//a[@class="icon_b i_map"]/../p')
            if len(eles) > 0:
                company['address'] = eles[0].text.strip()

            shop.saveShop(company)
            dr.close()
            dr.switch_to.window(dr.window_handles[-1])
            time.sleep(3)
        eles=dr.find_elements_by_xpath('//a[text()="下一页"]')
        if len(eles)>0:
            eles[0].click()
            current_page = dr.current_url
            tools.append(PAGE, 'w', current_page)
        else:
            break



while True:
    if current_page=='':
        tools.exe_wait(dr, '//*[@id="kwdselectid"]', '//div')
        dr.find_element_by_xpath('//*[@id="kwdselectid"]').clear()
        dr.find_element_by_xpath('//*[@id="kwdselectid"]').send_keys('招商'.decode('utf-8'))
        dr.find_element_by_xpath('//*[@id="select_expect_indtype"]').click()
        for li in dr.find_elements_by_xpath('//ul[@id="indtype_click_center_left"]/.//li'):
            flg=False
            li.click()
            tools.exe_wait(dr,'//div[@class="indtype_click_center_right_list de d3" and (@style="display: block;" or not(@style))]','//div')
            for em in dr.find_elements_by_xpath('//div[@class="indtype_click_center_right_list de d3" and (@style="display: block;" or not(@style))]/.//em'):
                word=em.get_attribute('innerHTML').strip()
                if word in skip_words:
                    continue
                else:
                    for selected in dr.find_elements_by_xpath('//div[@id="indtype_click_multiple_selected"]/span'):
                        selected.click()
                    em.click()
                    dr.find_element_by_xpath('//span[@id="indtype_click_bottom_save"]').click()
                    dr.find_element_by_xpath('//button[@class="p_but" and @type="submit"]').click()
                    current_page = dr.current_url
                    tools.append(PAGE, 'w', current_page)
                    tools.append(SKIP, 'a', word+"\n")
                    skip_words.add(word)
                    flg=True
                    break
            if flg:
                break;
    if current_page=='':
        break
    read(current_page)
    current_page=''


dr.quit()