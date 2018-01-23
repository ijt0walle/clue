# encoding: utf-8

from selenium import webdriver
import time
import sys
import tools
import shop as shoptool
from selenium.webdriver.common.action_chains import ActionChains
import traceback

'''设置编码'''
reload(sys)
sys.setdefaultencoding('utf-8')

main_dir='D:\\tmall'       #存放验证码、截屏等目录
current_page=''                  #当前翻页url地址
PAGE='D:\\tmall\\page'   #存放翻页url地址、断点执行
user='wgl1688123124234'       #登录名
password='123456wgl1688'      #登陆密码
token=''                       #百度api相关token（解析营业执照）
refresh_mod=1                  #模数（多任务隔离使用）
refresh_num=0                  #
top='食品'          #淘宝搜索关键词
#女鞋/男鞋/箱包     女装/内衣  男装/运动户外    美妆/个人护理  腕表/眼镜/珠宝饰品    手机/数码/电脑办公
#母婴玩具    零食/茶酒/进口食品     生鲜水果  大家电/生活电器   家具建材              汽车/配件/用品   家纺/家饰/鲜花  医药保健
#厨具/收纳/宠物


#获取上次执行到分页url
file_obj=open(PAGE)
for line in file_obj.readlines():
    current_page=line
file_obj.close()


search_url='https://shopsearch.taobao.com/search?app=shopsearch&commend=all&q=KEY_WORD&search_type=shop&loc=%E4%B8%8A%E6%B5%B7&isb=1'

'''begin'''
#经过浏览器设置
chrome_options = webdriver.ChromeOptions()
# PROXY = "121.43.189.255:84712394"
# chrome_options.add_argument('--proxy-server=%s' % PROXY)
# chrome_options.add_experimental_option("prefs",{"profile.managed_default_content_settings.images":2})
dr = webdriver.Chrome(executable_path="C:\Users\Administrator\Downloads\chromedriver_win32\chromedriver.exe",chrome_options=chrome_options)
tools.login(dr,user,password)
main_handler=dr.current_window_handle



if current_page == '':#如果不存在则从搜索进入
    dr.get(search_url.replace('KEY_WORD',top))
    tools.append(PAGE, 'w', dr.current_url)#保存url
else:
    dr.get(current_page)
pack={'class':top}
index=0
while True:
    tools.scrollToEnd(dr)#滚动到网页末尾
    time.sleep(1)
    shops=dr.find_elements_by_xpath('//a[@class="shop-name J_shop_name"]')#获取所有shop的链接url
    for shop in shops:
        try:
            shop_name = shop.text.strip()
            '''检查shop是否已经存在数据库'''
            if shoptool.isExsits(shop_name):
                print 'exits '+shop_name
                continue
            #打开shop的search页面
            dr.execute_script('window.open("' + 'https://'+shop.get_attribute("href").split('/')[2]+'/search.htm' + '");')
            dr.switch_to.window(dr.window_handles[-1])#切换到打开的新页面
            if len(dr.find_elements_by_xpath('//button[@id="J_CurrShopBtn"]')) == 0:  # 排除天猫自己的店铺
                continue
            while not tools.exe_wait(dr, '//a[@class="tm-gsLink"]', '//div[@class="main-info"]'):#等待a[@class="tm-gsLink"]出现，超时没有出现则进入while体
                eles=dr.find_elements_by_xpath('//a[@class="mui-dialog-close mui-overlay-close"]')
                if len(eles)>0:
                    eles[0].click()#如果是警告直接关闭
                else:
                    tools.login(dr,user,password)#重新登陆
                    dr.refresh()#刷新当前页面

            shop_dict = {'shop_name': shop_name,'index':index }
            index+=1
            goods_dict = {}
            shop_dict['describe'] = shoptool.extract(dr, "描述相符：")
            shop_dict['service'] = shoptool.extract(dr, "服务态度：")
            shop_dict['logistics'] = shoptool.extract(dr, "物流服务：")
            shop_dict['city'] = shoptool.extract_shop_city(dr)
            shop_dict['history'] = shoptool.extract_shop_time(dr)
            shop_dict['goods'] = shoptool.extract_goods(dr)
            shop_dict['class'] = pack['class']
            print len(shop_dict['goods'])
            '''
            解析验证码
            '''
            dr.get(dr.find_element_by_xpath('//a[@class="tm-gsLink"]').get_attribute('href'))
            while True:
                jpg_file = main_dir + '\\' + shop_name + '.jpg'
                png_file = main_dir + '\\screenshot.png'
                tools.snapshot(dr, '//img', png_file, jpg_file)  # 截取验证码
                code = tools.check_tmall_code(jpg_file)  # 解析验证码

                dr.find_element_by_xpath('//input[@name="checkCode"]').send_keys(code)
                dr.find_element_by_xpath('//button[text()="确定"]').click()
                if len(dr.find_elements_by_xpath('//div[@class="box-item img-box"]')) == 0:
                    time.sleep(1)
                    continue
                # 验证码检验通过
                jpg_file=dr.find_element_by_xpath('//img').get_attribute('src').split(',')[1].replace('&#10;','').replace('%0A','')#直接获取营业执照的base64
                break

            # 解析营业执照
            map1  = tools.get_business_license(jpg_file, token, 1, 0)  # 通过百度解析营业执照
            token = map1['token']
            map2 = tools.get_accurate_basic(jpg_file, token, 1, 0)  # 通过百度解析普通图片
            token = map2['token']
            if map1['words_result'].has_key('单位名称'):
                shop_dict['company_name'] = map1['words_result']['单位名称']['words']
            else:
                shop_dict['company_name'] = ''

            if map1['words_result'].has_key('法人'):
                shop_dict['legal_person'] = map1['words_result']['法人']['words']
            else:
                shop_dict['legal_person'] = ''

            if map1['words_result'].has_key('地址'):
                shop_dict['address'] = map1['words_result']['地址']['words']
            else:
                shop_dict['address'] = ''

            # 写入数据库
            shop_ext = {'img_business':map1,'img_basic':map2}
            shop_ext['goods'] = shop_dict['goods']
            shop_ext['shop_info'] = {
                'describe': shop_dict['describe'],
                'service': shop_dict['service'],
                'logistics': shop_dict['logistics'],
                'history': shop_dict['history']
            }
            shop_dict['ext'] = shop_ext
            shoptool.saveShop(shop_dict)#保存到数据库

            time.sleep(10)
        except Exception, e:
            time.sleep(5)
            print 'traceback.format_exc():\n%s' % traceback.format_exc()
        dr.close()
        dr.switch_to.window(main_handler)


    #准备翻页
    next=dr.find_elements_by_xpath('//li[@class="item next"]/a')
    if len(next)>0 :
        next[0].click()#翻页
        tools.append(PAGE, 'w', dr.current_url)
    else:
        break

dr.quit()#推出