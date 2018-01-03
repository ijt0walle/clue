#coding:utf-8
import datetime
import traceback
import json
import pymysql
import sys
from util import get_time


class Mysql_db:
    def __init__(self):
        self.conn=pymysql.connect(host='121.43.168.132',
                  user='maxwell',
                  port =3307,
                  passwd='ED81A84EC3B290A4EFA26122test',
                  db='test',charset="utf8")
        reload(sys)
        sys.setdefaultencoding('utf-8')

    def get_close(self):
        try:
            if self.conn is not None:
                self.conn.close()
        except Exception as e:
            print(str(e))

    # insert single record
    # def insert(self, name, company_name,clue_status,result,main_classi,page_home_url,page_achivers_url,classi_1,classi_2):
    #     cur = self.conn.cursor()
    #     try:
    #         sql = 'insert into test.' + str(name) + '(company_name,clue_status,updated_at,1688_result,main_classi,page_home_url,page_achivers_url,classi_1,classi_2) values(\"%s\",%d,\"%s\",\"%s\",\"%s\",\"%s\",\'\',\"%s\",\"%s\")' % (company_name,clue_status,get_time(),result,main_classi,page_home_url,classi_1,classi_2)
    #         print('%s:sql=%s' % (get_time(), sql))
    #         cur.execute(sql)
    #         self.conn.commit()
    #     except Exception as e:
    #         print(traceback.format_exc())
    #     finally:
    #         self.close_cur(cur)

    def excute(self,sql):
        cur = self.conn.cursor()
        try:
            print('%s:sql=%s' % (get_time(), sql))
            cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(traceback.format_exc())
        finally:
            self.close_cur(cur)

    # update some record from table
    def update_stauts(self, table_name,crawler_code,taobao_result,id):
        cur = self.conn.cursor()
        try:
            sql = 'update %s set crawler_code=%d, taobao_result=\"%s\", 1688_updated_time =\"%s\" where id=%d;' % (table_name,crawler_code,taobao_result,self.get_time(),id)
            cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print("Mysql Error %s" % (str(e)))
        finally:
            self.close_cur(cur)

    def update_company_page_home(self,table_name,crawler_code,page_home_url,result,id):
        cur = self.conn.cursor()
        try:
            sql = 'update %s set crawler_code=%d, page_home_url=\"%s\",taobao_result=\"%s\" ,1688_updated_time =\"%s\" where id=%d;' % (table_name,crawler_code,page_home_url,result,self.get_time(),id)
            cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print("Mysql Error %s" % (str(e)))
        finally:
            self.close_cur(cur)

    def update_company_search(self,table_name,main_classi,id):
        cur = self.conn.cursor()
        try:
            sql = 'update %s set main_classi=main_classi+\"%s\",updated_at= \"%s\" where id=%d;' % (
            table_name, main_classi, get_time(),id)
            cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print("Mysql Error %s" % (str(e)))
        finally:
            self.close_cur(cur)

    def insert(self,sql):
        id = 0
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            id = int(self.conn.insert_id())
            self.conn.commit()
            print('%s:sql=%s' % (get_time(), sql))
        except Exception as e:
            print('%s:sql=%s' % (get_time(), sql))
            print (e)
        finally:
            self.close_cur(cur)
        return id

    def update(self,sql):
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            self.conn.commit()
            print('%s:sql=%s' % (get_time(), sql))
        except Exception as e:
            print('%s:sql=%s' % (get_time(), sql))
            print (e)
        finally:
            self.close_cur(cur)

    def update_company_search(self, table_name, company_name,main_classi,home_page, result,status,id):
        cur = self.conn.cursor()
        try:
            sql = 'update %s set company_name = \"%s\",main_classi=\"%s\",page_home_url = \"%s\",1688_result = \"%s\",clue_status=%d, updated_at= \"%s\" where id=%d;' % (
                table_name, company_name,main_classi, home_page,result,status,get_time(), int(id))
            cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print("Mysql Error %s" % (str(e)))
        finally:
            self.close_cur(cur)

    def update_company_achivers(self, table_name, crawler_code, company_achivers_url, result, id):
        cur = self.conn.cursor()
        try:
            sql = 'update %s set crawler_code=%d, page_achivers_url=\"%s\",1688_result=\"%s\" ,1688_updated_time =\"%s\" where id=%d;' % (
            table_name, crawler_code, company_achivers_url, result, self.get_time(),id)
            cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print("Mysql Error %s" % (str(e)))
        finally:
            self.close_cur(cur)

    def get_sql_data(self,sql):
        cur = self.conn.cursor()
        results = None
        try:
            cur.execute(sql)
            self.conn.commit()
            results = list(cur.fetchall())
        except Exception as e:
            print ("Mysql Error %s" % str(e))
        finally:
           self.close_cur(cur)
        return results

    def get_from_company_name(self,table_name,company_name):
        cur = self.conn.cursor()
        results = None
        try:
            sql = 'select * from ' + str(table_name) + ' where company_name =\"%s\"' % company_name
            cur.execute(sql)
            self.conn.commit()
            results = list(cur.fetchall())
        except Exception as e:
            print ("Mysql Error %s" % str(e))
        finally:
           self.close_cur(cur)
        if results is not None and (len(results))>0:
            return results[0]
        return None

    def get_sql_crm_config(self,table_name,keyword):
        cur = self.conn.cursor()
        results = None
        try:
            sql = 'select * from %s where instr(region_over,%s)=0 ;' % (table_name,keyword)
            cur.execute(sql)
            self.conn.commit()
            results = list(cur.fetchall())
        except Exception as e:
            print ("Mysql Error %s" % str(e))
        finally:
           self.close_cur(cur)
        if results is not None and (len(results))>0:
            return results
        return None

    def get_crm_config(self,table_name,keyword):
        lists = self.get_sql_crm_config(table_name,keyword)
        if lists is None or len(lists) == 0:
            return []
        for l in lists:
            try:
                region_time = json.loads(l[7])
                updated_at = region_time.get(keyword)
                d1 = datetime.datetime.strptime(updated_at, '%Y-%m-%d %H:%M:%S')
                cur = datetime.datetime.now()
                if updated_at is None or (cur - d1).seconds > 12*60*60:
                    cnt  = int(json.loads(l[5]).get(keyword))
                    region_time[keyword] = cur
                    convert_result = json.dumps(region_time, ensure_ascii=False, encoding='UTF-8').encode("utf-8").replace("'", '"').replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
                    self.update('update %s set region_time = %s where id = %d' % (table_name,convert_result,int(l[0])))
                    return (l[0],l[3],cnt)
            except Exception as e:
                print e
        return (0,0,0)

    def select_condition(self,sql):
        cur = self.conn.cursor()
        results = []
        try:
            cur.execute(sql)
            cur.scroll(0, mode='absolute')  # reset cursor location (mode = absolute | relative)
            results = cur.fetchall()
        except Exception as e:
            print("Mysql Error %s" % (str(e)))
        finally:
            self.close_cur(cur)
        return results

    def close_cur(self,cur):
        try:
            if cur is not None:
                cur.close()
        except Exception as e:
            pass

    def get_time(self):
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")

    def get_one_clue(self,sql):
        result = self.select_condition(sql)[0]
        self.update('update 1688_clue set clue_status = 4 where id = '+str(result[0]))
        return result

    def __del__(self):
        try:
            if self.conn is not None:
                self.conn.close()
        except Exception as e:
            print(str(e))