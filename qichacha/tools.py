# encoding: utf-8

from PIL import Image
import pymysql as MySQLdb
import sys
import time
import httplib
import base64
import urllib
from selenium.webdriver.common.action_chains import ActionChains

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

def snapshot(dr,xpath,screenshotFile,imgFile):
    dr.save_screenshot(screenshotFile)
    imgelement = dr.find_element_by_xpath(xpath)
    location = imgelement.location  # 获取验证码x,y轴坐标
    size = imgelement.size  # 获取验证码的长宽
    rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
    int(location['y'] + size['height']))  # 写成我们需要截取的位置坐标
    i = Image.open(screenshotFile)  # 打开截图
    frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
    frame4.save(imgFile)


def readFromDB(host,user,passwd,db,port,sql,values):
    conn = MySQLdb.connect(host=host, user=user, passwd=passwd,db=db, charset='utf8', port=port)
    cur = conn.cursor()
    info = cur.fetchmany(cur.execute(sql,values))
    cur.close()
    conn.close()
    return info

def update_sql(sql):
    conn = MySQLdb.connect(host='121.43.168.132', user='maxwell', passwd='ED81A84EC3B290A4EFA26122test',db='test', charset='utf8', port=3307)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

def get_companies(source):
    pack= readFromDB('121.43.168.132', 'maxwell', 'ED81A84EC3B290A4EFA26122test', 'test', 3307,'select company_name from test.companies where company_name<>"" and isDelete=0 and '+source+'=0 limit 2', ())
    return pack

def get_data(sql):
    return readFromDB('121.43.168.132', 'maxwell', 'ED81A84EC3B290A4EFA26122test', 'test', 3307,sql,())


def saveShop(shop):
    if shop.get('phone') is None or len(shop.get('phone')) <=2:
        return
    executeDB('121.43.168.132', 'maxwell', 'ED81A84EC3B290A4EFA26122test', 'test', 3307,
                    'INSERT IGNORE INTO test.companies_detail (`company_name`,`legal_person`,`address`,`registered_capital`,`phone`,`mail`,`soruce`,`ext`) '
                    'VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
                    (shop.get('company_name'), shop.get('legal_person'), shop.get('address'), shop.get('registered_capital'),shop.get('phone'),shop.get('mail'), shop.get('soruce'), shop.get('ext')))

def saveCompany(company,source):
    executeDB('121.43.168.132', 'maxwell', 'ED81A84EC3B290A4EFA26122test', 'test', 3307,
                    'update test.companies set '+str(source)+' = 1 where company_name = %s', (company))

def executeDB(host,user,passwd,db,port,sql,values):
    conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, charset='utf8', port=port)
    cur = conn.cursor()
    cur.execute(sql,values)
    cur.close()
    conn.commit()
    conn.close()

def str_process(s):
    if s is None or len(s) == 0:
        return s
    return str(s).replace('（','').replace('）','').replace(')','').replace('(','').lower()

def get_access_token(mod,num):
    lis=readFromDB('121.43.168.132','maxwell','ED81A84EC3B290A4EFA26122test','test',3307,
               'select grant_type,client_id,client_secret,id from baidu_ocr_api where id%%'
                +str(mod)+'='+str(num)+'  order by check_time limit 1',())
    executeDB('121.43.168.132','maxwell','ED81A84EC3B290A4EFA26122test','test',3307,
              ' update baidu_ocr_api set check_time=%s where id=%s',
              (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),str(lis[0][3]))
              )
    url = '/oauth/2.0/token?grant_type='+lis[0][0].strip()+\
          '&client_id='+lis[0][1].strip()+'&client_secret='+lis[0][2].strip()
    conn = httplib.HTTPSConnection("aip.baidubce.com")
    conn.request(method="GET", url=url)
    response = conn.getresponse()
    res = eval(response.read())
    conn.close()
    return res['access_token']

def getImgBase64(file):
    f = open(file, 'rb')  # 二进制方式打开图文件
    ls_f = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
    f.close()
    return ls_f

def transImg(file,access_token):
    if len(file)<100:
        base64_str=getImgBase64(file)
    else:
        base64_str=file
    params = urllib.urlencode({
        'detect_direction':'true',
        'probability':'true',
        'image':base64_str
    })
    headers = {"Content-Type":"application/x-www-form-urlencoded"}
    conn = httplib.HTTPSConnection("aip.baidubce.com")
    conn.request(method="POST",url="/rest/2.0/ocr/v1/general_basic?access_token="+access_token,body=params,headers=headers)
    response = conn.getresponse()
    str= response.read()
    str= str.encode('utf-8')
    res = eval(str)
    conn.close()
    return res


def transBusiness(file,access_token):
    if len(file)<100:
        base64_str=getImgBase64(file)
    else:
        base64_str=file
    params = urllib.urlencode({
        'image':base64_str
    })
    headers = {"Content-Type":"application/x-www-form-urlencoded"}
    conn = httplib.HTTPSConnection("aip.baidubce.com")
    conn.request(method="POST",url="/rest/2.0/ocr/v1/business_license?access_token="+access_token,body=params,headers=headers)
    response = conn.getresponse()
    str= response.read()
    str= str.encode('utf-8')
    res = eval(str)
    conn.close()
    return res

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
        return default;
# def move(dr,a,b):


# map=transBusiness('C:\\Users\\wanggenlong\\Desktop\\tupian\\4.jpg',get_access_token(2,1))
# print json.dumps(map)

def check_tmall_code(file):
    f = urllib.urlopen("http://121.43.173.22:8070/taobao/captch?img="+urllib.quote(getImgBase64(file)))
    s = f.read().replace("\"","").replace("\n","").strip()
    return s


def get_business_license(file,access_token,refresh_mod,refresh_num):
    token=access_token
    if token=='':
        token=get_access_token(refresh_mod, refresh_num)
    map={}
    while True:
        map = transBusiness(file,token)
        if map.has_key('words_result'):
            break
        elif map.has_key('error_code') and (map['error_code']==216201 or map['error_code']==216202):
            break
        else:
            print map
            time.sleep(5)
            token=get_access_token(refresh_mod, refresh_num)
    map['token']=token#更新后的token
    return map


def get_accurate_basic(file,access_token,refresh_mod,refresh_num):
    token = access_token
    if token=='':
        token=get_access_token(refresh_mod, refresh_num)
    map = {}
    while True:
        map = transImg(file, token)
        if map.has_key('words_result'):
            break
        elif map.has_key('error_code') and (map['error_code']==216201 or map['error_code']==216202):
            break
        else:
            print map
            time.sleep(5)
            token = get_access_token(refresh_mod, refresh_num)
    map['token'] = token  # 更新后的token
    return map


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
