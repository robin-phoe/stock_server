import redis
import pymysql
import logging
import time
import datetime
import pandas as pd
import numpy as np
import re
import pub_uti_a
import json

logging.basicConfig(level=logging.CRITICAL, filename='../log/monitor.log', filemode='a',
                    format='%(asctime)s-%(levelname)5s: %(message)s')
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)





class bk_buffer:
    def __init__(self):
        self.bk_obj_buffer = {} #{bk_id:instance}
        self.df = None #stock_id bk 多对多
        self.bk_rank = {} #bk_code:rank
        self.bk_new_market= {}
        self.bk_set = set()
        self.init_bk_buffer()
        self.bk_increase = {}
    def init_bk_buffer(self):
        # 待优化，stock_information 表中没有bk_code ，须补上
        # sql = "select I.stock_id,I.bk_name,B.bk_code from stock_informations I " \
        #       " LEFT JOIN (select distinct bk_name,bk_code from bankuai_day_data " \
        #       " where trade_date = (select max(trade_date) as trade_date from bankuai_day_data)) B " \
        #       " ON I.bk_name = B.bk_name "
        sql = "select stock_id,bk_name,bk_code from stock_informations where bk_code is not null "
        self.df = pub_uti_a.creat_df(sql)
        self.bk_set = set(self.df['bk_code'].tolist())
        for bk_code in self.bk_set:
            single_df = self.df[self.df.bk_code == bk_code]
            self.bk_obj_buffer[bk_code] = bk(single_df)
    def refresh_market(self,stock_market):
        self.bk_new_market = r.hgetall("bk_single_market")
        self.sort_bk()
        self.refresh_bk_instance(stock_market)
    def sort_bk(self):
        for bk_code in self.bk_set:
            self.bk_increase[bk_code] = json.loads(self.bk_new_market[bk_code])['increase']
        mem_list = sorted(self.bk_increase.items(), key=lambda d: d[1], reverse=True)  # 倒序
        for i in range(len(mem_list)):
            self.bk_rank[mem_list[i][0]] = i+1
    def refresh_bk_instance(self,stock_market):
        # print('err:', self.bk_obj_buffer,self.bk_increase,self.bk_rank )
        for bk_code in self.bk_set:
            self.bk_obj_buffer[bk_code].real_time_refresh(stock_market,self.bk_increase[bk_code],self.bk_rank[bk_code])
    def get_bk_instance(self,bk_name):
        if bk_name not in self.bk_obj_buffer:
            return False
        else:
            return self.bk_obj_buffer[bk_name]
    def get_buffer_all_key(self):
        return self.bk_obj_buffer.keys()
class bk:
    def __init__(self,single_df):
        self.df = single_df
        self.name = None
        self.id = None
        self.members = [] #列表
        self.increase = 0  # 板块增长
        self.amount = 0  # 板块成交量
        self.member_real_info = {}  # 成员实时交易信息
        self.member_rank = {}  # 板块内成员排序
        self.mem_count = 0
        self.bk_rank = None
        self.init_bk_info()
    def init_bk_info(self):
        for index,raw in self.df.iterrows():
            self.name = raw['bk_name']
            self.id = raw['bk_code']
            self.members.append(raw['stock_id'])
        self.mem_count = len(self.members)
    def real_time_refresh(self,stock_market,bk_increase,bk_rank):
        self.increase = bk_increase
        self.bk_rank = bk_rank
        for id in self.members:
            if id not in stock_market:
                continue
            self.member_real_info[id] = json.loads(stock_market[id])['increase']
        self.__sort_member()
    def __sort_member(self):
        mem_list = sorted(self.member_real_info.items(), key=lambda d: d[1], reverse=True) #倒序
        for i in range(0,len(mem_list)):
            self.member_rank[mem_list[i][0]] = "{}/{}".format(str(i+1),self.mem_count)
    def get_rank_in_bk(self,stock_id):
        # print("member_rank",self.members,self.member_rank)
        return self.member_rank[stock_id]
    def get_bk_info(self):
        return (self.name,self.id,self.member,self.increase,self.amount)
class stock:
    def __init__(self,df_raw):
        self.stock_name = df_raw['stock_name']
        self.stock_id = df_raw['stock_id']
        self.bk_name = df_raw['bk_name']
        self.bk_code = df_raw['bk_code']
        self.grade = None
        self.timestamp = None
        self.base_grade = df_raw['grade']
        self.monitor_type = df_raw['monitor_type']
        self.in_bk_rank = None
        self.bk_increase = None
        self.increase = None
        self.price = None
        self.return_data = None
        self.hot_concept = None
        self.hot_concept_increase = None
        self.bk_sort =None
        self.in_sort =None
        self.concept_list=[]

    def refresh_data(self,market,bk_obj_buffer):
        bk = bk_obj_buffer[self.bk_code]
        single_market = json.loads(market)
        self.timestamp = market['timestamp']
        self.price = single_market['price']
        self.increase = single_market['increase']
        self.grade = self.increase
        self.bk_increase = bk.increase
        self.bk_sort = bk.bk_rank
        self.in_sort = bk.get_rank_in_bk(self.stock_id)
        self.concept_list = [self.bk_name] #临时
        self.hot_concept = bk.name  #临时
        self.hot_concept_increase = bk.increase  #临时
        self.return_data = {
            "id":self.stock_id,
            "timestamp":self.timestamp,
            "name":self.stock_name,
            "grade":self.grade,
            "price":self.price,
            "increase":self.increase,
            "bk":self.bk_name,
            "bk_increase":self.bk_increase,
            "bk_sort":self.bk_sort,
            "in_sort":self.in_sort,
            "concept_list":self.concept_list,
            "hot_concept":self.hot_concept,
            "hot_concept_increase":self.hot_concept_increase,
            "monitor_type":self.monitor_type,
            }
class stock_buffer:
    def __init__(self):
        self.stock_dict = {}  # {stock_id:instance}
        self.monitor_df = None
        self.new_market_name = "single_market"
        self.all_market_name = "day_market"
        self.new_market = None
        self.timestamp = None
        self.stock_obj_buffer = {}
        self.algo_monitor_name = "algo_monitor"
        self.all_algo_monitor_name = "all_algo_monitor"
        self.monitor_stockid_buffer = []
        self.algo_monitor_data = {}
    def init_monitor_buffer(self,set_date = None):
        if set_date == None:
            sql = "select date_format(max(trade_date) ,'%Y-%m-%d') as trade_date from monitor"
            monitor_date = pub_uti_a.select_from_db(sql)[0][0]
        else:
            monitor_date = set_date
        print('监控日期：',monitor_date)
        sql = "select M.monitor,I.stock_id,I.stock_name,M.grade,M.monitor_type,I.bk_name,I.bk_code from stock_informations I " \
              " INNER JOIN (select * from monitor  where trade_date = '{}') M" \
              " ON M.stock_id = I.stock_id " \
              " where I.bk_code is not null " .format(monitor_date) #where I.bk_code is not null 数据不一致，暂时
        self.monitor_df = pub_uti_a.creat_df(sql)
        print('监控数量：{}'.format(len(self.monitor_df)))
        # 待加入：删除含空值行
        self.monitor_stockid_buffer = self.monitor_df['stock_id'].to_list()
        # self.monitor_df.reset_index('stock_id',inplace=True)
        self.init_stocks()
    def init_stocks(self):
        for index,raw in self.monitor_df.iterrows():
            self.stock_obj_buffer[raw['stock_id']] = stock(raw)
    def get_redis_market(self):
        self.new_market = r.hgetall(self.new_market_name)
        self.timestamp = self.new_market['timestamp']
    def refresh_stocks(self,bk_buffer):
        # print("new_market",self.new_market)
        for id in self.monitor_stockid_buffer:
            self.stock_obj_buffer[id].refresh_data(self.new_market[id],bk_buffer)
            #存储algo
            stock_message = self.stock_obj_buffer[id].return_data
            r.hset(self.algo_monitor_name,id,json.dumps(stock_message, indent=2, ensure_ascii=False))
            #储存algo全量
            if (r.hexists(name=self.all_algo_monitor_name, key=id)):
                all_algo_message = json.loads(r.hget(self.all_algo_monitor_name, id))
            else:
                all_algo_message = {}
            all_algo_message[self.timestamp] = stock_message
            r.hset(self.all_algo_monitor_name, id, json.dumps(self.all_algo_monitor_name,
                                                                  indent=2, ensure_ascii=False))

        print('algo 已存入 redis。')


def run():
    s_buffer = stock_buffer()
    s_buffer.init_monitor_buffer()
    b_buffer = bk_buffer()
    b_buffer.init_bk_buffer()

    start_t_com = datetime.datetime.now()
    s_buffer.get_redis_market()
    b_buffer.refresh_market(s_buffer.new_market)
    s_buffer.refresh_stocks(b_buffer.bk_obj_buffer)
    print('计算耗时：', datetime.datetime.now() - start_t_com)


if __name__ == '__main__':
    start_t = datetime.datetime.now()
    run()
    print('耗时：',datetime.datetime.now() - start_t)
