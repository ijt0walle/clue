# encoding: utf-8

from PIL import Image
import sys
import time


'''设置编码'''
reload(sys)
sys.setdefaultencoding('utf-8')

def getShopInfo(dr,company_name):

    dr.find_element_by_xpath('//input[@id="headerKey"]').clear()
    dr.find_element_by_xpath('//input[@id="headerKey"]').send_keys(company_name.decode())
    dr.find_element_by_xpath('//button[@type="submit"]').click()
    conpanys = dr.find_elements_by_xpath('//table[@class="m_srchList"]/.//tr')
    list_company_infos = []
    for tr in conpanys:
        rt = {}
        # search_company = tr.find_element_by_xpath('/a[@class="ma_h1"]').text
        # rt['公司名称'] = search_company
        # eles = tr.find_elements_by_xpath('//p[@class="m-t-xs" and contains(text(),"法定代表人：")]/a')
        # if len(eles) > 0: rt['法人'] = eles[0].text
        # eles = tr.find_elements_by_xpath('//span[@class="m-l" and contains(text(),"注册资本：")]')
        # if len(eles) > 0: rt['注册资本'] = eles[0].text.replace('注册资本：','').strip()
        # eles = tr.find_elements_by_xpath('//span[@class="m-l" and contains(text(),"成立时间：")]')
        # if len(eles) > 0: rt['成立时间'] = eles[0].text.replace('成立时间：','').strip()
        # eles = tr.find_elements_by_xpath('//p[@class="m-t-xs" and contains(text(),"电话：")]')
        # if len(eles) > 0: rt['电话'] = eles[0].text.replace('电话：', '').strip().split('邮箱')[0].strip()
        # eles = tr.find_elements_by_xpath('//span[contains(text(),"邮箱：") and @class="m-l"]')
        # if len(eles) > 0: rt['邮箱'] = eles[0].text.replace('邮箱：', '').strip()
        # eles = tr.find_elements_by_xpath('//p[@class="m-t-xs" and contains(text(),"地址：")]')
        # if len(eles) > 0: rt['地址'] = eles[0].text.replace('地址：', '').strip()
        strs = (tr.text).replace("\n"," ").replace("：",":").split(" ")
        if len(strs) < 3:
            continue
        rt['公司名称'] = strs[0]
        for i in range(1,len(strs)):
            s = strs[i]
            st = s.split(":")
            if len(st) == 2:
                s0 = str(st[0])
                s1 = st[1]
                rt[s0] = s1
        list_company_infos.append(rt)
    if (conpanys is None or len(conpanys) == 0):
        text = dr.find_element_by_xpath('//*[@id="smartBox"]/div[1]')
        if text is None:
            time.sleep(180)
        else:
            return list_company_infos
    return list_company_infos

