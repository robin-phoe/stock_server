
#coding=utf-8
import requests
import re
import pymysql
import logging
import json
import datetime
import time
from multiprocessing import Pool
import redis
import pub_uti_a

logging.basicConfig(level=logging.INFO,filename="../log/real_trade_data.log",filemode="w",
                    format="%(asctime)s-%(levelname)5s: %(message)s")

count=0
r = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)
r.pubsub()
"""
获取单个页面股票数据
{name:F14,最新价:F2,涨跌幅:F3,成交量:F5,ID:F12,成交额:F6,振幅:F7,最高:F15,最低:F16,今开:F17,昨收:F18,量比:F10,换手:F8,市盈(动):F9,市净率:F23}
"""
def getOnePageStock(timestamp):
    global count,r
    url = "http://18.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112406268274658974922_1605597357094&pn=1" \
          "&pz=5000&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13," \
          "m:0+t:80,m:1+t:2,m:1+t:23&fields=f2,f3,f4,f5,f6,f8,f10,f12,f14,f15,f16,f17&_=1605597357108"
    #url = "http://18.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112406268274658974922_1605597357094&pn=2&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1605597357108"
    #print("url:",url)
    header={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"}
    response = requests.get(url,headers=header)
    text=response.text
    result = re.findall("\[.*?\]", text)
    # print("result:",result)
    if len(result) == 0:
        return 0
    else:
        Data_json = json.loads(result[0])
        #print(Data_json)
    time_trade_to_redis(Data_json,timestamp)


"""
日内行情保存至redis
single_market={
    id:{
        "timestamp":timestamp,
        "id": id, 
        "name": name, 
        "price": price, 
        "increase": increase, 
        "volume": volume,
        "volume_rate": volume_rate, 
        "turnover": turnover, 
        "volume_money": volume_money
        }
    }
day_market={
    id:{
            timestamp:{
                "timestamp":timestamp,
                "id": id, 
                "name": name, 
                "price": price, 
                "increase": increase, 
                "volume": volume,
                "volume_rate": volume_rate, 
                "turnover": turnover, 
                "volume_money": volume_money
            },
            timestamp:{
                ···
            }
        }
    }
"""
def time_trade_to_redis(Data_json,timestamp):
    for data in Data_json:
        # 清理可能为 - 的数据值
        for key in data:
            if data[key] == "-":
                data[key] = 0
        # timestamp = datetime.datetime.now().timestamp()
        id = data["f12"]
        name = data["f14"]
        price = data["f2"]
        increase = data["f3"]
        high_price = data["f15"]
        low_price = data["f16"]
        open_price = data["f17"]
        volume_rate = data["f10"]
        turnover = data["f8"]
        volume_money = data["f6"]
        volume = data['f5']


        single_market = "single_market"
        day_market = "day_market"
        # 判断id 在hash中是否存在
        if (r.hexists(name=day_market, key=id)):
            old_market = json.loads(r.hget(single_market,id))
            # print('volume_check:',old_market["volume"],old_market["name"])
            volume -= old_market["volume"]
            new_market = {"timestamp":timestamp,"id": id, "name": name, "price": price, "increase": increase, "volume": volume,
                          "volume_rate": volume_rate, "turnover": turnover, "volume_money": volume_money}
            all_market_str = r.hget(day_market,id)
            all_market_json = json.loads(all_market_str)
        else:
            new_market = {"timestamp":timestamp,"id": id, "name": name, "price": price, "increase": increase, "volume": volume,
                          "volume_rate": volume_rate, "turnover": turnover, "volume_money": volume_money}
            all_market_json = {}
        all_market_json[timestamp] = new_market
        r.hset(single_market, id,json.dumps(new_market, indent=2, ensure_ascii=False))
        r.hset(day_market, id, json.dumps(all_market_json, indent=2, ensure_ascii=False))
    r.publish('trigger_flag', "true")
    return 1
"""
获取日内板块信息
{name:f14,id:f12,price:f2,increase:f3,total_value:total_value,turnover:f8,up:f104,down:f105}
"""
def get_bk_info(timestamp):
    global r
    url = "http://44.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112404219198714508219_1607384110344&pn=1&pz=100&po=1&np=1&" \
          "ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:90+t:2+f:!50&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12," \
          "f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107,f104,f105,f140,f141,f207," \
          "f208,f209,f222&_=1607384110349"

    header={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"}
    response = requests.get(url,headers=header)
    text=response.text
    result = re.findall("\[.*?\]", text)
    # print("result bk:",result)
    if len(result) == 0:
        return 0
    else:
        Data_json = json.loads(result[0])
        #print(Data_json)
    bk_to_redis(Data_json,timestamp)

"""
板块行情保存至redis
bk_single_market={
    "id":{
    "timestamp":timestamp,
    "id": id, 
    "name": name, 
    "price": price, 
    "increase": increase,
    "volume": volume, 
    "turnover": turnover,
    "up":up,
    "down":down
    }
}
bk_day_market={
    "id":{
        "time_stamp":{
                "timestamp":timestamp,
                "id": id, 
                "name": name, 
                "price": price, 
                "increase": increase,
                "volume": volume, 
                "turnover": turnover,
                "up":up,
                "down":down
            }
    }
}
"""
def bk_to_redis(Data_json,timestamp):
    for data in Data_json:
        # 清理可能为 - 的数据值
        for key in data:
            if data[key] == "-":
                data[key] = 0
        # timestamp = datetime.datetime.now().timestamp()
        id = data["f12"]
        name = data["f14"]
        price = data["f2"]
        increase = data["f3"]
        total_value = data["f20"]/100000000 #换算成亿
        turnover = data["f8"]
        up = data["f104"]
        down = data['f105']
        volume = total_value * (turnover/100)


        single_market = "bk_single_market"
        day_market = "bk_day_market"
        # 判断id 在hash中是否存在
        if (r.hexists(name=day_market, key=id)):
            old_market = json.loads(r.hget(single_market,id))
            # print('volume_check:',old_market["volume"],old_market["name"])
            volume -= old_market["volume"]
            new_market = {"timestamp":timestamp,"id": id, "name": name, "price": price, "increase": increase,
                          "volume": volume, "turnover": turnover,"up":up,"down":down}
            all_market_str = r.hget(day_market,id)
            all_market_json = json.loads(all_market_str)
            all_market_json[timestamp] = new_market
        else:
            new_market = {"timestamp":timestamp,"id": id, "name": name, "price": price, "increase": increase,
                          "volume": volume, "turnover": turnover}
            all_market_json = {timestamp:new_market}

        r.hset(single_market, id,json.dumps(new_market, indent=2, ensure_ascii=False))
        r.hset(day_market, id, json.dumps(all_market_json, indent=2, ensure_ascii=False))
    return 1
"""
个股、板块单次页面获取
"""
def main():
    # print("时间1:",datetime.datetime.now().strftime("%H:%M:%S,%f"))
    # print("page:",page)
    timestamp = datetime.datetime.now().timestamp()
    getOnePageStock(timestamp)
    get_bk_info(timestamp)

"""
日交易结束，redis分时行情保存到mysql
"""
def save_to_mysql(date = None):
    if date == None:
        date = datetime.datetime.now().strftime("%Y-%m-%d")
    #存储股票分时数据
    all_market_json = r.hgetall('day_market')
    sv = pub_uti_a.save()
    for id in all_market_json:
        sql = "INSERT INTO miu_trade_data (stock_id,trade_date,data) values ('{0}','{1}','{2}')".format(id,date,all_market_json[id])
        sv.add_sql(sql)
    sv.commit()
    print('股票分時數據存儲完成')
    #存储algo分时数据
    all_market_json = r.hgetall('all_algo_monitor')
    sv = pub_uti_a.save()
    for id in all_market_json:
        sql = "INSERT INTO algo_miu_data (stock_id,trade_date,data) values ('{0}','{1}','{2}')".format(id,date,all_market_json[id])
        sv.add_sql(sql)
    sv.commit()
    print('algo分時數據存儲完成')
    #存储板块分时数据
    all_market_json = r.hgetall('bk_day_market')
    sv = pub_uti_a.save()
    for id in all_market_json:
        sql = "INSERT INTO bk_miu_data (bk_id,trade_date,data) values ('{0}','{1}','{2}')".format(id,date,all_market_json[id])
        sv.add_sql(sql)
    sv.commit()
    print('板塊分時數據存儲完成')


"""
run
"""
def run():
    i=0
    end_trade_flush= False
    start_trade_flush = True
    while True:
        time_now = datetime.datetime.now().strftime("%H:%M:%S")
        weekday = datetime.datetime.now().weekday()
        # if True:
        if weekday < 5 and  time_now >= "09:20:00" and time_now <= "15:01:00" :
            #集合竞价、午盘休息暂停
            if  (time_now > "11:31:00" and time_now <= "13:00:00")  :
                time.sleep(1)
                continue
            # 开盘清理redis
            if start_trade_flush ==True and time_now <= "09:31:00":
                r.flushdb()
                print("已清空redis")
                start_trade_flush = False
                end_trade_flush = True
            print(time_now)
            time1 = datetime.datetime.now()
            main()
            time2 = datetime.datetime.now()
            time_delta = time2 - time1
            print("时间:",i,  time2.strftime("%H:%M:%S,%f"))
            print("时间差:",time_delta)
            i+=1
            time.sleep(40)
        #收盘redis持久化
        elif end_trade_flush == True:
            save_to_mysql()
            end_trade_flush = False
            start_trade_flush = True
        time.sleep(1)
if __name__ == "__main__":
    run()
    # main()
    # save_to_mysql('2021-10-08')



