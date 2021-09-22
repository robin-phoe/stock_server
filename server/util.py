import pub_uti_a
import json
import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

"""
获取k线数据
Request:
{
    type:'monitor', #"all","single","monitor","retracement","single_limit"
    traget_date:'' #监控模式下必填
    start_date:'2021-02-01',
    end_date:'2021-09-08',
    stock_id:''
}
Response:
// id:[id,trade_date,open_price,close_price,low_price,high_price,turnover_rate,point_type,0,0,0]
{
    "002962":[
       ["002962","2020-01-03",12.1,12.5,11.9,12.9,2.1,"n",0,0,0],
       ["002962","2020-01-04",12.5,12.7,12.1,12.85,2.3,"h",0,0,0],
       ···
      ]
    "002963":[
       ···
      ]
}
"""
def get_kline(request):
    request_param = json.loads(request.body)
    response_json = {"code": 200, "message": "请求成功", "data": ""}
    if request.method != 'POST':
        response_json = {"code": 502, "message": "请求方法错误", "data": ""}
        return response_json
    # 查询字段sql
    filed_sql = 'select stock_id,date_format(trade_date ,"%Y-%m-%d") as trade_date,open_price,close_price,' \
                'low_price,high_price,turnover_rate,point_type,0 as a,0 as b,0 as c  ' \
                ' from stock_trade_data '
    start_date = request_param["start_date"]
    end_date = request_param["end_date"]
    traget_date = get_last_monitor_date(request_param["traget_date"])
    table_map = {"monitor":"monitor", "retracement":"remen_retracement", "single_limit":"limit_up_single"}
    #查询单支股票
    if request_param["type"] == 'single':
        id_tuple = (request_param["stock_id"],request_param["stock_id"])
        where_sql = " where stock_id in {0} and trade_date >= '{1}' and trade_date <= '{2}'" \
                    "".format(id_tuple, start_date, end_date)
    #查询监控类股票
    elif request_param["type"] in table_map:
        sql = "select stock_id from {} where trade_date = '{}'" \
              "".format(table_map[request_param["type"]],traget_date)
        id_tuple_res = pub_uti_a.select_from_db(sql)
        id_list = []
        for id in id_tuple_res:
            id_list.append(id[0])
        id_tuple = tuple(id_list)
        print('id_tuple:',id_tuple)
        where_sql = " where stock_id in {0} and trade_date >= '{1}' and trade_date <= '{2}'" \
                    "".format(id_tuple, start_date, end_date)
    #查询所有股票
    elif request_param["type"] == 'all':
        where_sql = " where  trade_date >= '{0}' and trade_date <= '{1}'" \
                    "".format(start_date, end_date)
    else:
        print('ERROR')
        response_json = {"code": 502, "message": "type不符合", "data": ""}
        return response_json

    sql = filed_sql + where_sql
    print('sql:',sql)
    df = pub_uti_a.creat_df(sql)
    df['point_type'] = df['point_type'].apply(lambda x: 'n' if x == '' else x)
    df = df[["stock_id","trade_date","open_price","close_price","low_price","high_price","turnover_rate","point_type","a","b","c"]]
    # 行转换为列表
    rows_list = df.values.tolist()
    kline_json = {}
    for row in rows_list:
        id = row[0]
        if id in kline_json:
            kline_json[id].append(row)
        else:
            kline_json[id] = [row]
    # response_json['data'] = json.dumps(kline_json, indent=2, ensure_ascii=False)
    response_json['data'] = kline_json

    return response_json

def time_line(request):
    request_param = json.loads(request.body)
    response_json = {"code": 200, "message": "请求成功", "data": ""}
    if request.method != 'POST':
        response_json = {"code": 502, "message": "请求方法错误", "data": ""}
        return response_json
    monitor_type = request_param["type"]
    target_date = get_last_monitor_date(request_param["target_date"])
    if monitor_type == "single":
        id_tuple = ((request_param["stcok_id"],),)
    else:
        type_map = {"monitor":'',"retracement":'remen_retra',"single_limit":'single_limit_retra'}
        sql = "select stock_id from monitor where trade_date = '{}' and monitor_type like '{}%'".format(target_date,type_map[monitor_type])
        id_tuple = pub_uti_a.select_from_db(sql) #((id,),())
    return_data = []
    hash_name = "day_market"
    for id_tup in id_tuple:
        id = id_tup[0]
        algo_single = r.hget(hash_name,id)
        print('redis_res',algo_single)
        if algo_single != None:
            return_data.append(json.loads(r.hget(hash_name,id)))

    # eg_data = [
    #     {
    #         "id":"003853",
    #         "name":"洪都航空",
    #         "grade":105.1,
    #         "price":39.5,
    #         "increase":9.0,
    #         "bk":"航空航天",
    #         "bk_increase":3.25,
    #         "bk_sort":2,
    #         "in_sort":5,
    #         "concept":"大飞机",
    #         "concept_increase":5,
    #         "monitor_type":"热门回撤",
    #     },
    #     {
    #         "id":"002963",
    #         "name":"比亚迪",
    #         "grade":95.1,
    #         "price":239.5,
    #         "increase":4.0,
    #         "bk":"汽车整车",
    #         "bk_increase":2.15,
    #         "bk_sort":4,
    #         "in_sort":9,
    #         "concept":"锂电池",
    #         "concept_increase":1,
    #         "monitor_type":"单涨停回撤",
    #     },
    #     ]

    response_json['data'] = return_data
    return response_json

"""
获取k线数据
Request:
{
    type:'monitor', #"all","single","monitor","retracement","single_limit"
    traget_date:'' #监控模式下必填
    start_date:'2021-02-01',
    end_date:'2021-09-08',
    stock_id:''
}
Response:
// id:[id,trade_date,open_price,close_price,low_price,high_price,turnover_rate,point_type,0,0,0]
{
    "002962":[
       ["002962","2020-01-03",12.1,12.5,11.9,12.9,2.1,"n",0,0,0],
       ["002962","2020-01-04",12.5,12.7,12.1,12.85,2.3,"h",0,0,0],
       ···
      ]
    "002963":[
       ···
      ]
}
"""
def get_bk_kline(request):
    request_param = json.loads(request.body)
    response_json = {"code": 200, "message": "请求成功", "data": ""}
    if request.method != 'POST':
        response_json = {"code": 502, "message": "请求方法错误", "data": ""}
        return response_json
    # 查询字段sql
    filed_sql = 'select bk_code,date_format(trade_date ,"%Y-%m-%d") as trade_date,open_price,close_price,' \
                'low_price,high_price,turnover_rate,0 as a,0 as b,0 as c,0 as d  ' \
                ' from bankuai_day_data '

    start_date = request_param["start_date"]
    end_date = request_param["end_date"]
    #查询单支股票
    if request_param["type"] == 'single':
        where_sql = " where bk_code = '{0}' and trade_date >= '{1}' and trade_date <= '{2}'" \
                    "".format(request_param["bk_id"], start_date, end_date)
    #查询所有股票
    elif request_param["type"] == 'all':
        where_sql = " where  trade_date >= '{0}' and trade_date <= '{1}'" \
                    "".format(start_date, end_date)
    else:
        print('ERROR')
        response_json = {"code": 502, "message": "type不符合", "data": ""}
        return response_json

    sql = filed_sql + where_sql
    print('sql:',sql)
    df = pub_uti_a.creat_df(sql)
    df = df[["bk_code","trade_date","open_price","close_price","low_price","high_price","turnover_rate","a","b","c","d"]]
    # 行转换为列表
    rows_list = df.values.tolist()
    kline_json = {}
    for row in rows_list:
        id = row[0]
        if id in kline_json:
            kline_json[id].append(row)
        else:
            kline_json[id] = [row]
    # response_json['data'] = json.dumps(kline_json, indent=2, ensure_ascii=False)
    response_json['data'] = kline_json

    return response_json

def bk_time_line(request):
    request_param = json.loads(request.body)
    response_json = {"code": 200, "message": "请求成功", "data": ""}
    if request.method != 'POST':
        response_json = {"code": 502, "message": "请求方法错误", "data": ""}
        return response_json
    type = request_param["type"]
    target_date = get_last_monitor_date(request_param["target_date"])
    # if type == "single":
    #     id_tuple = ((request_param["bk_id"],),)
    # else:
    #
    #     sql = "select stock_id from monitor where trade_date = '{}' and monitor_type like '{}%'".format(target_date,type_map[monitor_type])
    #     id_tuple = pub_uti_a.select_from_db(sql) #((id,),())
    return_data = []
    hash_name = "bk_day_market"
    if type == "single":
        bk_day_market = return_data.append(json.loads(r.hget(hash_name,request_param["bk_id"])))
    else:
        bk_day_market = r.hgetall(hash_name)
        for bk_id in bk_day_market:
            return_data.append(json.loads(bk_day_market[bk_id]))

    response_json['data'] = return_data
    return response_json
"""
获取algo实时数据
Request：
{  
    "type:"monitor",  
    "traget_date":"None" #有监控结果的最后一日  
}
Response:
{
    "code":"200",
    "message":"请求成功",
    "data":{  
        "003853":{
                "id":"003853",
                "name":"洪都航空",
                "grade":105.1,
                "price":39.5,
                "increase":9.0,
                "bk":"航空航天",
                "bk_increase":3.25,
                "bk_sort":2,
                "in_sort":5,
                "concept":"大飞机",
                "concept_increase":5,
                "monitor_type":"热门回撤",
            }
        "002963":{
                ···
            }
        }
}
"""
def get_algo(request):
    request_param = json.loads(request.body)
    response_json = {"code": 200, "message": "请求成功", "data": ""}
    if request.method != 'POST':
        response_json = {"code": 502, "message": "请求方法错误", "data": ""}
        return response_json
    monitor_type = request_param["type"]
    target_date = get_last_monitor_date(request_param["target_date"])
    type_map = {"monitor":'',"retracement":'remen_retra',"single_limit":'single_limit_retra'}
    sql = "select stock_id from monitor where trade_date = '{}' and monitor_type like '{}%'".format(target_date,type_map[monitor_type])
    id_tuple = pub_uti_a.select_from_db(sql) #((id,),())
    return_data = []
    hash_name = "algo_monitor"
    for id_tup in id_tuple:
        id = id_tup[0]
        algo_single = r.hget(hash_name,id)
        print('redis_res',algo_single)
        if algo_single != None:
            return_data.append(json.loads(r.hget(hash_name,id)))

    # eg_data = [
    #     {
    #         "id":"003853",
    #         "name":"洪都航空",
    #         "grade":105.1,
    #         "price":39.5,
    #         "increase":9.0,
    #         "bk":"航空航天",
    #         "bk_increase":3.25,
    #         "bk_sort":2,
    #         "in_sort":5,
    #         "concept":"大飞机",
    #         "concept_increase":5,
    #         "monitor_type":"热门回撤",
    #     },
    #     {
    #         "id":"002963",
    #         "name":"比亚迪",
    #         "grade":95.1,
    #         "price":239.5,
    #         "increase":4.0,
    #         "bk":"汽车整车",
    #         "bk_increase":2.15,
    #         "bk_sort":4,
    #         "in_sort":9,
    #         "concept":"锂电池",
    #         "concept_increase":1,
    #         "monitor_type":"单涨停回撤",
    #     },
    #     ]

    response_json['data'] = return_data
    return response_json
# 辅助函数
def get_last_monitor_date(traget_date):
    if traget_date != 'None':
        return traget_date
    sql = "select max(trade_date) from monitor"
    last_date = pub_uti_a.select_from_db(sql)[0][0]
    return last_date
