# coding=utf-8
import sys
import urllib
import json

reload(sys)
sys.setdefaultencoding('utf-8')


TOKEN = "8b64638da7690c376d0a1b9c1495ef060d79be4822496a71"

def get_api_data(company_name):
    clue_id = search_api_company_name(company_name)
    if clue_id == 0:
        return {}
    company_info = get_api_company_info(clue_id)
    return company_info


def search_api_company_name(company_name):
    company_urlencode = str(urllib.quote(company_name))
    request = 'https://api.datatist.cn/v2/api/autocompleteCname.jsp?keyword=%s&token=%s' % (company_urlencode,TOKEN)
    results = urllib.urlopen(request).read()
    try:
        j = json.loads(results)
        id = j['messages']['data'][0].get('id')
        title = j['messages']['data'][0].get('title').replace('(','').replace(')','').replace('（','').replace('）','')
        if title.find(company_name) >= 0:
            return id
    except Exception as e:
        print company_name + ' api no data'
    print 0



def get_api_company_info(clueId):
    request = "https://api.datatist.cn/v2/api/detail.jsp?id=%s&token=%s" %(clueId,TOKEN);
    results = urllib.urlopen(request).read()
    dict = {}
    try:
        j = json.loads(results)
        try:
            dict['国家']=j['messages']['data']['brief']['country']
        except Exception as e : pass
        try:
            dict['城市'] = j['messages']['data']['brief']['city']
        except Exception as e : pass
        try:
            dict['成立时间'] = j['messages']['data']['brief']['foundDate']
        except Exception as e: pass
        try:
            dict['法人']=j['messages']['data']['json']['base_info']['legal_person']
        except Exception as e: pass
        try:
            dict['注册资本']=j['messages']['data']['json']['base_info']['register_capital']
        except Exception as e: pass
    except Exception as e:
        print e

    except Exception as e:
        print str(clueId) + ' api no data'
    print 0
    return results

get_api_data('点点客上海')
