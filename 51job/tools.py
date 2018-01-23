# encoding: utf-8

from PIL import Image
import MySQLdb
import sys
import time
import httplib
import base64
import urllib
from selenium.webdriver.common.action_chains import ActionChains
import json

'''设置编码'''
reload(sys)
sys.setdefaultencoding('utf-8')


'''write file'''
def append(def_file_name,def_flg,def_line):
    def_file_obj=open(def_file_name, def_flg)
    def_file_obj.write(def_line)
    def_file_obj.close()

def scrollToEnd(dr):
    index=10
    while True:
        index+=10
        js = "document.documentElement.scrollTop="+str(index)
        dr.execute_script(js)
        if index>=10000:
            break


def readFromDB(host,user,passwd,db,port,sql,values):
    conn = MySQLdb.connect(host=host, user=user, passwd=passwd,db=db, charset='utf8', port=port)
    cur = conn.cursor()
    info = cur.fetchmany(cur.execute(sql,values))
    cur.close()
    conn.close()
    return info

def executeDB(host,user,passwd,db,port,sql,values):
    conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, charset='utf8', port=port)
    cur = conn.cursor()
    cur.execute(sql,values)
    cur.close()
    conn.commit()
    conn.close()


def getImgBase64(file):
    f = open(file, 'rb')  # 二进制方式打开图文件
    ls_f = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
    f.close()
    return ls_f



def wait(dr,xpath):
    i = 0
    while True:
        if i>=30:
            break
        if len(dr.find_elements_by_xpath(xpath)) > 0:
            break
        else:
            time.sleep(0.1)
            i += 1

def exe_wait(dr,xpath,xpath2):
    i=0
    while True:
        if i>=30:
            return False
        ActionChains(dr).move_to_element(dr.find_element_by_xpath(xpath2)).perform()
        if len(dr.find_elements_by_xpath(xpath)) > 0:
            break
        else:
            time.sleep(0.1)
            i+=1
    return True

def floatOrDefault(x,default):
    try:
        return float(x)
    except:
        return default




def login(dr,user,password):
    dr.delete_all_cookies()
    dr.execute_script('window.open("https://login.tmall.com");')
    dr.switch_to.window(dr.window_handles[-1])
    '''登陆'''
    dr.switch_to.frame(0)
    dr.find_element_by_xpath('//div[@class="login-switch"]').click()

    ActionChains(dr).move_to_element(dr.find_element_by_xpath('//input[@id="TPL_username_1"]')).perform()
    i = 0
    while i < 20:
        ActionChains(dr).move_by_offset(1, 1).perform()
        time.sleep(0.05)
        i += 1

    dr.find_element_by_xpath('//input[@id="TPL_username_1"]').send_keys(user)
    dr.find_element_by_xpath('//input[@id="TPL_password_1"]').send_keys(password)
    dr.find_element_by_xpath('//button[@id="J_SubmitStatic"]').click()
    if len(dr.window_handles)>0:
        dr.close()
        dr.switch_to.window(dr.window_handles[-1])
