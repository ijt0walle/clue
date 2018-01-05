# coding=utf-8
import sys

import time
from lxml import etree

from util import stringQ2B, process_str


class parse_1688:
    count = 5
    company = ''
    time_sleep = 2000

    def set_reslut_item(self,result_item):
        self.resultItem = result_item

    def __init__(self, kw,result_item):
        if result_item is not None:
            self.resultItem = result_item
        else:
            self.resultItem = {}
        self.company = kw
        reload(sys)
        sys.setdefaultencoding('utf-8')

    def parse_list_search(self,html1):
        list = []
        html = None
        try:
            html = etree.HTML(html1)
        except:
            return
        url = ''
        # 公司名称
        aa = html.xpath('//*[@id="sw_mod_searchlist"]/ul/*');
        for i in range(0,len(aa)):
            reslutItem = self.get_offer_info(html,i+1)
            list.append(reslutItem)
        return list


    def get_offer_info(self,html,i):
        resultItem = {}
        try:
            company_name = html.xpath('//*[@id="offer%d"]/div[1]/div[2]/div[1]/a[1]' % i)
            new_company = stringQ2B(company_name[0].get('title')).lower().strip().replace(')', '').replace('(', '')
            resultItem['company'] = new_company
            url = company_name[0].get("href")
            resultItem['url'] = url
        except Exception as e:
            print (str(resultItem.get('company')) + str('公司名称不存在'))

        # 公司主营
        try:
            main_c = html.xpath('//*[@id="offer%d"]/div[1]/div[2]/div[3]/div[1]/div[1]/a/*' % i);
            main_d = []
            for i in range(0, len(main_c)):
                main_d.append(main_c[i].text)
            resultItem['main_d'] = process_str(','.join(main_d))
        except Exception as e:
            print (str(resultItem.get('company')) + str(':公司主营解析错误'))

        # 公司地址
        try:
            resultItem['address'] = process_str(html.xpath('//*[@id="offer%d"]/div[1]/div[2]/div[3]/div[1]/div[2]/a' % i)[0].text)
        except Exception as e:
            print (str(resultItem.get('company')) + str(':公司地址解析错误'))

        try:
            resultItem['shop_name'] = process_str(html.xpath('//*[@id="offer%d"]/div[1]/div[2]/div[2]/span' % i)[0].text)
        except Exception as e:
            print (str(resultItem.get('company')) + str(':店铺名称解析错误'))

        # 公司人数
        try:
            resultItem['company_persons'] = process_str(html.xpath('//*[@id="offer%d"]/div[1]/div[2]/div[3]/div[1]/div[3]/a' % i)[0].get('title'))
        except Exception as e:
            print (str(resultItem.get('company')) + str('公司人数解析错误'))

        # 贸易类型
        try:
            resultItem['model'] = html.xpath('//*[@id="offer%d"]/div[1]/div[2]/div[3]/div[2]/div[1]/b' % i)[0].text
        except Exception as e:
            print (str(resultItem.get('company')) + str('贸易类型解析错误'))
        #
        for j in range(1,4):
            try:
                resultItem[html.xpath('//*[@id="offer%d"]/div[1]/div[2]/div[3]/div[2]/div[%d]/span' % (i,j+1))[0].text] = html.xpath('//*[@id="offer%d"]/div[1]/div[2]/div[3]/div[2]/div[%d]/a' % (i,j+1))[0].text
            except Exception as e:
                pass
        return resultItem

    def company_baseinfo(self, html1):
        try:
            html = etree.HTML(html1)
        except:
            return
        url = ''
        # 公司名称
        try:
            company_name = html.xpath('//*[@id="offer1"]/div[1]/div[2]/div[1]/a[1]');
            new_company = stringQ2B(company_name[0].get('title')).lower().strip().replace(')','').replace('(','')
            if cmp(new_company, self.company) != 0:
                print (self.company + ",公司名称不相等")
                return 1;
            self.resultItem['company'] = process_str(company_name[0].get('title'))
            url = company_name[0].get("href")
            self.resultItem['url'] = url
        except Exception as e:
            print (str(self.company) + str('公司名称不存在'))
            return 3

        # 公司主营
        try:
            main_c = html.xpath('//*[@id="offer1"]/div[1]/div[2]/div[3]/div[1]/div[1]/a/*');
            main_d = []
            for i in range(0, len(main_c)):
                main_d.append(main_c[i].text)
            self.resultItem['main_d'] = ','.join(main_d)
        except Exception as e:
            print (str(self.company) + str(e.message))

        # 公司地址
        try:
            self.resultItem['address'] = html.xpath('//*[@id="offer1"]/div[1]/div[2]/div[3]/div[1]/div[2]/a')[0].text
        except Exception as e:
            print (str(self.company) + str(e.message))

        # 公司人数
        try:
            self.resultItem['company_persons'] = html.xpath('//*[@id="offer1"]/div[1]/div[2]/div[3]/div[1]/div[3]/a')[0].get('title')
        except Exception as e:
            print (str(self.company) + str(e.message))

        # 贸易类型
        try:
            self.resultItem['model'] = html.xpath('//*[@id="offer1"]/div[1]/div[2]/div[3]/div[2]/div[1]/b')[0].text
        except Exception as e:
            print (str(self.company) + str(e.message))

        return url

    def parse_company_captial(self, html1):
        try:
            html = etree.HTML(html1)
        except:
            return
        url = ''
        # 公司名称
        self.get_goods_title(html)
        #公司
        try:
            self.resultItem['classifications'] = "".join(html.xpath('//meta[@name="keywords"]/@content'))
        except Exception as e:
            print (str(self.company) + str(e.message))
        # 公司的价格
        try:
            item_prices = html.xpath('//em/text()')
            item_price = []
            for price in item_prices:
                try:
                    p = float(price.strip().strip('\r').strip('\n').strip('\t'))
                    item_price.append(p)
                except Exception as e:
                    pass
            size = len(item_price)
            #print item_price
            if size > 1:
                item_price.sort()
                self.resultItem['max_price'] = item_price[size - 1]
                self.resultItem['min_price'] = item_price[1]
                self.resultItem['unit_price'] = sum(item_price) / size
                self.resultItem['mid_price'] = item_price[size / 2]
        except Exception as e:
            print (str(self.company) + str(e.message))
        try:
            url = self.get_page_native(html)
        except Exception as e:
            print e;
        return url;


    def get_page_native(self,html):
        #公司档案
        contactinfo = ''
        try:
            company_info_url = html.xpath('//*[@id="site_header"]/div/div[2]/div/div[2]/div/div/ul/*/*')
            if company_info_url is None or len(company_info_url)<2:
                company_info_url =html.xpath('//*[@id="site_header"]/div/div/div[2]/div/div[2]/div/div/ul/*/*')
            if company_info_url is None or len(company_info_url) < 2:
                company_info_url = html.xpath('//*[@id="site_header"]/div/div[2]/div/div[2]/div/div/ul/*/*')
            for i in range(0, len(company_info_url)):
                if  str(company_info_url[i].text).find('档案') >=0:
                    print '%s->%s->%s' % (self.company,company_info_url[i].text,company_info_url[i].get('href'))
                    contactinfo = company_info_url[i].get('href')
                if str(company_info_url[i].text).find('联系') >=0 and len(str(contactinfo))<5:
                    contactinfo = company_info_url[i].get('href')
                if str(company_info_url[i].text).find('代理') >=0:
                     self.resultItem['agent'] = 1
        except Exception as e:
            print (str(self.company) + str(e.message))
        if len(str(contactinfo))<5:
            return self.get_huangye(html)
        return contactinfo

    def get_achivers(self,html):
        contactinfo = ''
        try:
            company_info_url = html.xpath('//*[@id="site_header"]/div/div[2]/div/div[2]/div/div/ul/*/*')
            if company_info_url is None or len(company_info_url) <2:
                company_info_url = html.xpath('//*[@id="site_header"]/div/div/div[2]/div/div[2]/div/div/ul/*/*')
            for i in range(0, len(company_info_url)):
                if str(company_info_url[i].text).find('档案') >= 0:
                    print '%s->%s->%s' % (self.company, company_info_url[i].text, company_info_url[i].get('href'))
                    contactinfo = company_info_url[i].get('href')
                if str(company_info_url[i].text).find('联系') >= 0 and len(str(contactinfo)) > 5:
                    contactinfo = company_info_url[i].get('href')
                if str(company_info_url[i].text).find('代理') >= 0:
                    self.resultItem['agent'] = 1
        except Exception as e:
            print (str(self.company) + str(e.message))

    def parse_company_info(self, html1):
        # 公司信息
        try:
            html = etree.HTML(html1)
        except:
            return
        try:
            self.resultItem['shop_long'] = html.xpath('//a[@href="https://cxt.1688.com/"]/text()')
        except Exception as e:
            print (str(self.company) + str(e.message))

        #联系人姓名
        self.resultItem['contact_name'] = self.get_contact_name(html)

        #电话号码
        self.resultItem['telphone'] = self.get_telphone(html)

        #手机号码
        self.resultItem['phone'] = self.get_phone(html)
        #经营年份
        try:
            self.resultItem['bus_year'] = html.xpath(
                '//*[@id="site_content"]/div/div/div/div[2]/div/div[2]/div/div[1]/div/div/h1/a[2]/text()')
        except Exception as e:
            print (str(self.company) + str(e.message))

        #信用等级
        self.resultItem['credit_level'] = process_str(self.get_credit_level(html))

        #公司简介
        self.resultItem['company_intro'] = process_str(self.get_company_intro(html))

        #公司经营品牌
        self.resultItem['brand']= process_str(self.get_company_brand(html))

        #旺旺号码
        self.resultItem['wang_wang'] = process_str(self.get_wangwang(html))

        #注册资本
        self.resultItem['registered_capital'] = process_str(self.get_original_money(html))

        self.get_trade_credit_record(html)
        self.get_buyer_service_ablity(html)
        return 1

    def get_goods_title(self,html):
        try:
            list = []
            titles = html.xpath("//*[@class='offer-list-row']/li/div[3]/a/@title")
            index = 0
            for title in titles:
                list.append(str(index)+":"+process_str(title))
                index += 1
                if index > 20:
                    break
            self.resultItem['goods_title'] = "@@".join(list)
        except Exception as e:
            print (str(self.company) + str(e.message)+",contact_name")

    def get_huangye(self,html):
        status = 2
        try:
            company_intro = html.xpath('//*[@id="site_content"]/div[1]/div/div[1]/div/div[2]/div[2]/span')[0].text
            if company_intro is None or len(str(company_intro))<5:
                company_intro= html.xpath('//*[@id="site_content"]/div[1]/div/div/div/div[2]/div[2]/span/text()')
            self.resultItem['company_intro'] = process_str(company_intro)
        except Exception as e:
            print (str(self.company) + str(e.message) + ",company_intro")
        try:
            company_hidder = html.xpath('//*[@id="site_content"]/div[1]/div/div[1]/div/div[2]/p')[0].text
            if company_hidder is None or str(company_hidder)< 5:
                company_hidder = html.xpath('//*[@id="site_content"]/div[1]/div/div/div/div[2]/p')[0].text
            self.resultItem['company_hidder'] = process_str(company_hidder)
            self.resultItem['title'] = process_str(html.xpath('/html/head/title')[0].text)
        except:
            print (str(self.company) + str(e.message) + ",company_hidder")
        try:
            self.resultItem['classifications'] = process_str(html.xpath('//meta[@name="keywords"]/@content'))
        except:
            print (str(self.company) + str(e.message) + ",classifications")
        return status


    def parse_contactinfo(self,html1):
        try:
            html = etree.HTML(html1)
        except:
            return
        try:
            contact_name = html.xpath('//*[@id="site_content"]/div[1]/div/div/div/div[2]/div/div[1]/div[1]/dl/dd/a[1]')[0]
            self.resultItem['contact_name'] = str(contact_name.text)
        except Exception as e:
            print (str(self.company) + str(e.message)+",contact_name")
        try:
            self.resultItem['telphone'] = html.xpath('//*[@id="site_content"]/div[1]/div/div/div/div[2]/div/div[1]/div[2]/div[2]/dl[1]/dd')[0].text
        except Exception as e:
            print (str(self.company) + str(e.message) + ",telphone")
        try:
            self.resultItem['telphone'] = html.xpath('//*[@id="site_content"]/div[1]/div/div/div/div[2]/div/div[1]/div[2]/div[2]/dl[2]/dd')[0].text
        except Exception as e:
            pass
        try:
            self.resultItem['phone'] = html.xpath('//*[@id="site_content"]/div[1]/div/div/div/div[2]/div/div[1]/div[2]/div[2]/dl[1]/dd')[0].text
        except Exception as e:
            pass

    def get_trade_credit_record(self,html):
        try:
            self.resultItem['trade_cnt'] = html.xpath('//*[@id="J_CompanyTradeCreditRecord"]/ul/li[1]/p[2]')[0].text.strip().strip('\r').strip('\n').strip('\t')
            self.resultItem['trade_avg_cnt'] = html.xpath('//*[@id="J_CompanyTradeCreditRecord"]/ul/li[1]/p[5]')[0].text.strip().strip('\r').strip('\n').strip('\t')
            self.resultItem['trade_user_cnt'] = html.xpath('//*[@id="J_CompanyTradeCreditRecord"]/ul/li[2]/p[2]')[0].text.strip().strip('\r').strip('\n').strip('\t')
            self.resultItem['trade_avg_user_cnt'] = html.xpath('//*[@id="J_CompanyTradeCreditRecord"]/ul/li[2]/p[5]')[0].text.strip().strip('\r').strip('\n').strip('\t')
            self.resultItem['repeat_buy_ratio'] = html.xpath('//*[@id="J_CompanyTradeCreditRecord"]/ul/li[3]/p[2]')[0].text.strip().strip('\r').strip('\n').strip('\t')
            self.resultItem['repeat_avg_buy_ratio'] = html.xpath('//*[@id="J_CompanyTradeCreditRecord"]/ul/li[3]/p[5]')[0].text.strip().strip('\r').strip('\n').strip('\t')
            self.resultItem['refound_90_ratio'] = html.xpath('//*[@id="J_CompanyTradeCreditRecord"]/ul/li[4]/p[2]')[0].text.strip().strip('\r').strip('\n').strip('\t')
            self.resultItem['refound_avg_90_ratio'] = html.xpath('//*[@id="J_CompanyTradeCreditRecord"]/ul/li[4]/p[5]')[0].text.strip().strip('\r').strip('\n').strip('\t')
            self.resultItem['complain_90_ratio'] = html.xpath('//*[@id="J_CompanyTradeCreditRecord"]/ul/li[5]/p[2]')[0].text.strip().strip('\r').strip('\n').strip('\t')
            self.resultItem['complain_avg_90_ratio'] = html.xpath('//*[@id="J_CompanyTradeCreditRecord"]/ul/li[5]/p[5]')[0].text.strip().strip('\r').strip('\n').strip('\t')
            self.resultItem['dispute_90_ratio'] = html.xpath('//*[@id="J_CompanyTradeCreditRecord"]/ul/li[6]/p[2]')[0].text.strip().strip('\r').strip('\n').strip('\t')
            self.resultItem['dispute_avg_90_ratio'] = html.xpath('//*[@id="J_CompanyTradeCreditRecord"]/ul/li[6]/p[5]')[0].text.strip().strip('\r').strip('\n').strip('\t')
        except Exception as e:
            print (str(self.company) + 'get_trade_credit_record  is None')

    def get_buyer_service_ablity(self,html):
        try:
            type = html.xpath('//*[@id="J_DynamicScoreListMain"]/ul/li[1]/p[3]/span/span')[0].text.strip().strip('\r').strip('\n').strip('\t')
            describe = html.xpath('//*[@id="J_DynamicScoreListMain"]/ul/li[1]/p[4]')[0].text.strip().strip('\r').strip('\n').strip('\t').replace('%','')
            if type.find('低于')<0:
                self.resultItem['trade_cnt'] = (int(describe))*-1

            type = html.xpath('//*[@id="J_DynamicScoreListMain"]/ul/li[2]/p[3]/span/span')[0].text.strip().strip('\r').strip('\n').strip('\t')
            response_speed = html.xpath('//*[@id="J_DynamicScoreListMain"]/ul/li[2]/p[4]')[0].text.strip().strip('\r').strip('\n').strip('\t').replace('%','')
            if type.find('低于')<0:
                self.resultItem['trade_cnt'] = (int(response_speed))*-1

            type = html.xpath('//*[@id="J_DynamicScoreListMain"]/ul/li[3]/p[3]/span/span')[0].text.strip().strip('\r').strip('\n').strip('\t')
            fahuo_speed = html.xpath('//*[@id="J_DynamicScoreListMain"]/ul/li[3]/p[4]')[0].text.strip().strip('\r').strip('\n').strip('\t').replace('%','')
            if type.find('低于')<0:
                self.resultItem['trade_cnt'] = (int(fahuo_speed))*-1
        except Exception as e:
            print (str(self.company) + 'trade count is None')

    def get_company_brand(self,html):
        try:
            brand = html.xpath('//*[@id="site_content"]/div/div/div/div[2]/div/div[2]/div/div[1]/div/p[2]')[0].text
            return brand
        except Exception as e:
            pass
        try:
            brand = html.xpath('//*[@id="site_content"]/div/div/div/div[2]/div/div[2]/div/div[1]/div/p[2]')[0].text
            return brand
        except Exception as e:
            pass
        print (str(self.company) + 'brand is None')
        return None

    def get_original_money(self,html):
        try:
            company_intro = html.xpath('//*[@id="site_content"]/div/div/div/div[2]/div/div[2]/div/div[2]/div[2]/table/tbody/tr[2]/td[2]/p/span[1]')[0].text
            return company_intro
        except Exception as e:
            pass
        return None

    def get_company_intro(self,html):
        try:
            company_intro = html.xpath('//*[@id="J_COMMON_CompanyInfoDetailInfo"]/span')[0].text
            return company_intro
        except Exception as e:
            pass
        try:
            company_intro = html.xpath('//*[@id="J_COMMON_CompanyInfoSimpleInfo"]/span')[0].text
            return company_intro
        except Exception as e:
            pass
        print (str(self.company) + 'company_intro is None')
        return None


    def get_phone(self,html):
        try:
            phone = html.xpath('//*[@id="J_STRENGTH_CompanyInfoPhoneShow"]/span[2]')[0].text
            return phone
        except Exception as e:
            pass
        try:
            phone = html.xpath('//*[@id="J_COMMON_CompanyInfoPhoneShow"]/span[2]')[0].text
            return phone
        except Exception as e:
            pass
        print (str(self.company) + 'phone level is None')
        return None

    def get_contact_name(self,html):
        try:
            contact_name = html.xpath('//span[@id="J_STRENGTH_CompanyContact"]/text()')[0].strip()
            return contact_name
        except Exception as e:
            pass
        try:
            contact_name = html.xpath('//*[@id="J_COMMON_CompanyContact"]/span')[0].text
            return contact_name
        except Exception as e:
            pass
        print (str(self.company) + 'get_contact_name level is None')
        return None

    def get_telphone(self,html):
        telphone = None
        try:
            telphone = html.xpath(
                '//span[@id="J_STRENGTH_CompanyInfoTelShow"]//span[@class="tip-info phone-num"]/text()')
            if telphone is not None and len(str(telphone))>4:
                return telphone
        except Exception as e:
            print (str(self.company) + str(e.message))
        try:
            telphone = html.xpath('//*[@id="J_COMMON_CompanyInfoTelShow"]/span[2]')[0].text
        except Exception as e:
            print (str(self.company) + str(e.message))
        return telphone

    def get_credit_level(self,html):
        try:
            credit_level = html.xpath('//*[@id="site_content"]/div/div/div/div[2]/div/div[2]/div/div[1]/div/div/h1/a[3]')[0].text
            return credit_level
        except Exception:
            pass
        try:
            credit_level = html.xpath('//*[@id="site_content"]/div/div/div/div[2]/div/div[2]/div/div[1]/div/div[1]/h1/a[2]')[0].text
            return credit_level
        except Exception:
            pass
        print (str(self.company) + 'credit_level level is None')
        return None

    def get_wangwang(self,html):
        try:
            wang_wang = html.xpath('//*[@id="J_STRENGTH_CompanyContact"]/a')[0].get('href').split('uid=')[1].split('&')[0]
            return wang_wang
        except Exception:
            pass
        try:
            wang_wang = html.xpath('//*[@id="J_COMMON_CompanyContact"]/a')[0].get('href').split('uid=')[1].split('&')[0]
            return wang_wang
        except Exception:
            pass
        print (str(self.company) + 'get_wangwang level is None')
        return None

    def get_page_size(self,html1):
        page_size = 0
        try:
            html = etree.HTML(html1)
        except:
            return
        # 公司名称
        try:
            page_size = html.xpath('//*[@id="sw_mod_pagination_form"]/div/span')[0].text
            page_size = int(page_size[1:len(page_size) - 1])
        except Exception:
            pass
        return page_size



