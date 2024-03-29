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
from com_grade import compute_algo_grade

logging.basicConfig(level=logging.CRITICAL, filename='../log/monitor.log', filemode='a',
                    format='%(asctime)s-%(levelname)5s: %(message)s')
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

s_buffer = None
b_buffer = None
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
            res = self.bk_new_market.get(bk_code,None)
            if res:
                self.bk_increase[bk_code] = json.loads(res)['increase']
        mem_list = sorted(self.bk_increase.items(), key=lambda d: d[1], reverse=True)  # 倒序
        for i in range(len(mem_list)):
            self.bk_rank[mem_list[i][0]] = i+1
    def refresh_bk_instance(self,stock_market):
        # print('err:', self.bk_obj_buffer,self.bk_increase,self.bk_rank )
        for bk_code in self.bk_set:
            if bk_code in self.bk_obj_buffer and bk_code in self.bk_increase and bk_code in self.bk_rank:
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
        if stock_id in self.member_rank:
            return self.member_rank[stock_id]
        else:
            return -1
    def get_bk_info(self):
        return (self.name,self.id,self.member,self.increase,self.amount)
class stock:
    def __init__(self,df_raw):
        self.stock_name = df_raw['stock_name']
        self.stock_id = df_raw['stock_id']
        self.bk_name = df_raw['bk_name']
        self.bk_code = df_raw['bk_code']
        self.grade = 0
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
        self.volume_rate = None #量比
        self.turnover = None
        self.volume = None
        self.time_line_df = pd.DataFrame(columns=('timestamp','increase','price','volume_rate','turnover',
                                                  'volume'))

    def refresh_data(self,market,bk_obj_buffer):
        bk = bk_obj_buffer[self.bk_code]
        single_market = json.loads(market)
        self.timestamp = single_market['timestamp']
        self.price = single_market['price']
        self.increase = single_market['increase']
        self.bk_increase = bk.increase
        self.bk_sort = bk.bk_rank
        self.in_sort = bk.get_rank_in_bk(self.stock_id)
        self.concept_list = [self.bk_name] #临时
        self.hot_concept = bk.name  #临时
        self.hot_concept_increase = bk.increase  #临时
        # print('len(self.time_line_df):',len(self.time_line_df),self.time_line_df)
        self.volume_rate = single_market['volume_rate']
        self.turnover = single_market['turnover']
        self.volume = single_market['volume']
        self.time_line_df.loc[len(self.time_line_df)] = [self.timestamp,self.increase,self.price,
                                                         self.volume_rate,self.turnover,self.volume]
        # print('df:',self.time_line_df)
        #计算grade
        # self.algo_com_grade()
        self.return_data = {
            "id":self.stock_id,
            "timestamp":self.timestamp,
            "name":self.stock_name,
            # "grade":self.grade,
            "grade": self.increase * 15,
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
    """
    程序核心。最理想100分，每项满分时inc在2.5-4
    每项各自100分，乘权重后汇总100分。
    inc超过理想区域后，其他分数总和越高，inc罚分越少，反之越多，以筛除虚拉回落，强势但高inc突破100分。分时做为入手信号，是总分的把控机制，inc未超出理想区域的总分压制在100一下，超出的要助力推出100，虚拉的要压下总分
    """
    def algo_com_grade(self):
        self.grade = compute_algo_grade(self.base_grade,self.increase,self.bk_sort,self.bk_increase,self.in_sort,
                                        self.time_line_df)
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
            monitor_date = (datetime.datetime.strptime(set_date,'%Y-%m-%d')-datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        print('监控日期：',monitor_date)
        sql = "select M.monitor,I.stock_id,I.stock_name,M.grade,M.monitor_type,I.bk_name,I.bk_code from stock_informations I " \
              " INNER JOIN (select * from monitor  where trade_date = '{}') M" \
              " ON M.stock_id = I.stock_id " \
              " where I.bk_code is not null " .format(monitor_date) #where I.bk_code is not null 数据不一致，暂时
        print('sql:',sql)
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
    def refresh_stocks(self,bk_buffer):
        # print("new_market",self.new_market)
        for id in self.monitor_stockid_buffer:
            if id not in self.stock_obj_buffer or id not in self.new_market:
                continue
            self.stock_obj_buffer[id].refresh_data(self.new_market[id],bk_buffer)
            #存储algo
            stock_message = self.stock_obj_buffer[id].return_data
            self.timestamp = self.stock_obj_buffer[id].timestamp
            r.hset(self.algo_monitor_name,id,json.dumps(stock_message, indent=2, ensure_ascii=False))
            #储存algo全量
            if (r.hexists(name=self.all_algo_monitor_name, key=id)):
                all_algo_message = json.loads(r.hget(self.all_algo_monitor_name, id))
            else:
                all_algo_message = {}
            all_algo_message[self.timestamp] = stock_message
            r.hset(self.all_algo_monitor_name, id, json.dumps(all_algo_message,
                                                                  indent=2, ensure_ascii=False))

        print('algo 已存入 redis。')

def run():
    def init():
        global s_buffer, b_buffer
        s_buffer = stock_buffer()
        s_buffer.init_monitor_buffer()
        b_buffer = bk_buffer()
        b_buffer.init_bk_buffer()
        print('初始化完成。')
    def refresh():
        global s_buffer, b_buffer
        s_buffer.get_redis_market()
        b_buffer.refresh_market(s_buffer.new_market)
        s_buffer.refresh_stocks(b_buffer.bk_obj_buffer)
    init()
    init_flag = True
    ps = r.pubsub()
    ps.subscribe(['trigger_flag'])
    # for item in ps.listen():
    #     time_now = datetime.datetime.now().strftime("%H:%M:%S")
    #     if time_now >= "09:00:00" and time_now <= "10:00:00":
    #         if init_flag:
    #             init()
    #             init_flag = False
    #     else:
    #         init_flag = True
    #     start_t = datetime.datetime.now()
    #     refresh()
    #     print('耗时：',datetime.datetime.now() - start_t)
    while True:
        start_t = datetime.datetime.now()
        refresh()
        print('耗时：', datetime.datetime.now() - start_t)
        time.sleep(10)


def hostory_com(date):
    single_market = 'single_market'
    bk_single_market = 'bk_single_market'
    all_algo_monitor = 'all_algo_monitor'
    algo_monitor = 'algo_monitor'
    day_market = 'day_market'
    def clean():
        r.delete(single_market)
        r.delete(bk_single_market)
        r.delete(all_algo_monitor)
        r.delete(algo_monitor)
        r.delete(day_market)
    def select_from_db(date):
        miu_trade_dic = {}
        bk_trade_dic = {}
        sql = "select stock_id,data from miu_trade_data where trade_date = '{}'".format(date)
        miu_trade_res = pub_uti_a.select_from_db(sql)
        len_content = 0
        for stock in miu_trade_res:
            miu_trade_dic[stock[0]] = json.loads(stock[1])
            len_content = len(miu_trade_dic[stock[0]])
        sql = "select bk_id,data from bk_miu_data where trade_date = '{}'".format(date)
        bk_trade_df_res = pub_uti_a.select_from_db(sql)
        for bk in bk_trade_df_res:
            bk_trade_dic[bk[0]] = json.loads(bk[1])
        return miu_trade_dic,bk_trade_dic,len_content
    def init(date):
        global s_buffer, b_buffer
        s_buffer = stock_buffer()
        s_buffer.init_monitor_buffer(date)
        b_buffer = bk_buffer()
        b_buffer.init_bk_buffer()
        print('初始化完成。')
    def refresh():
        global s_buffer, b_buffer
        s_buffer.get_redis_market()
        b_buffer.refresh_market(s_buffer.new_market)
        s_buffer.refresh_stocks(b_buffer.bk_obj_buffer)

    clean()
    init(date)
    miu_trade_dic, bk_trade_dic,len_content = select_from_db(date)
    print('len_content:',len_content)
    for i in range(len_content):
        for stock in miu_trade_dic:
            miu_content = miu_trade_dic[stock]
            miu_keys_list = list(miu_content.keys())
            miu_new_market = miu_content[miu_keys_list[i]]
            r.hset(single_market, stock, json.dumps(miu_new_market, indent=2, ensure_ascii=False))
            if (r.hexists(name=day_market, key=stock)):
                all_market_str = r.hget(day_market, stock)
                all_market_json = json.loads(all_market_str)
            else:
                all_market_json ={}
            all_market_json[miu_new_market['timestamp']] = miu_new_market
            r.hset(day_market, stock, json.dumps(all_market_json, indent=2, ensure_ascii=False))
        for bk in bk_trade_dic:
            bk_content = bk_trade_dic[bk]
            bk_keys_list = list(bk_content.keys())
            bk_new_market = bk_content[bk_keys_list[i]]
            r.hset(bk_single_market, bk, json.dumps(bk_new_market, indent=2, ensure_ascii=False))
        refresh()



if __name__ == '__main__':
    run()
    # hostory_com(date = '2022-07-13')