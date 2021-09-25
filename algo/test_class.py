import pub_uti_a
sql = "select bk_name,bk_code from bankuai_day_data where trade_date = (select max(trade_date) from bankuai_day_data)"
res = pub_uti_a.select_from_db(sql)
res_dict = dict(res)
print('res:',res_dict)

s = pub_uti_a.save()
for key in res_dict:
    sql = "update stock_informations set bk_code = '{}' where bk_name = '{}'".format(res_dict[key],key)
    s.add_sql(sql)
s.commit()
