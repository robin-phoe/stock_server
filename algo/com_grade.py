from fractions import Fraction
import datetime
import copy
#负责具体分数的计算
'''
        self.grade = 0
        #基础日K分数
        base_grade_power = 0.8
        base_grade = 0
        if self.base_grade >= 20000:
            base_grade = 100
        elif self.base_grade >=10000:
            base_grade = (self.base_grade - 10000)/100
        self.grade += base_grade * base_grade_power
        #板块分数
        #大盘分数
        # 分时涨幅分数（分数K线的一部分）
        increase_power = 0.7
        inc_grade = 0
        if self.increase <= 0:
            inc_grade = 0
        elif 0 < self.increase < 2.5:
            inc_grade = 100 * self.increase/2.5
        elif 2.5 <= self.increase < 3.5:
            inc_grade = 100
        else:
            pass
        self.grade += inc_grade * increase_power
        #临时
        if self.increase >= 9.75:
            self.grade = 150
'''
'''
基础日K分数转换
'''
def base_grade_com(base_grade):
    grade = 0
    # 基础日K分数
    base_grade_power = 0.7
    if base_grade >= 30000:
        grade = 100
    elif base_grade >= 10000:
        grade = (base_grade - 10000) / 200
    grade = grade * base_grade_power
    return grade
'''
板块分数
1:板块热度(板块实时热度(排行、inc、流入资金)，板块历史热度)
2:个股在板块排名
热度100 * 内排名权重
'''
def bk_grade(bk_sort,bk_inc,in_sort):
    grade = 0
    bk_grade_power = 0.5
    ##板块实时热度
    #inc 30
    if bk_inc >= 3:
        grade += 30
    else:
        grade += (bk_inc + 1) * 7.5
    #bk_sort 30
    if bk_sort <= 3:
        grade += 30
    elif bk_sort <= 7:
        grade += 20
    else:
        grade += 30/((bk_sort - 7)**0.5) -10
    #资金
    grade += 20

    #内排名 str
    in_sort = Fraction(in_sort)
    #-x**2
    mul = float(-(in_sort**2) + 1)
    if mul < 0.1:
        mul = 0.1
    grade = grade * mul * bk_grade_power
    return grade
'''
大盘分数
'''
def market_grade():
    pass
'''
timeline 分数
计算前提：条/分钟行情
'''
def time_line_grade(df):
    grade = 0
    time_line_power = 0.5
    last_index = len(df) - 1
    timestamp = float(df.loc[last_index, 'timestamp'])
    time = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
    #平均值,5分钟均线，条/分钟
    df['inc_mean'] = df['increase'].expanding(1).mean()
    df['volume_mean'] = df['increase'].expanding(1).mean()
    df['mean_5'] = df['increase'].rolling(5).mean()
    df['mean_30'] = df['increase'].rolling(30).mean()
    df.fillna(0,inplace = True)

    inc = df.loc[last_index, 'increase']
    #根据涨幅加减分数 20
    if inc < 3.5:
        inc_grade = 6*inc
    else:
        inc_grade = 0
    # 计算拉升速率 30
    df['inc_delta_1'] = df['increase'] - df['increase'].shift(1)
    df['inc_delta_3'] = df['increase'] - df['increase'].shift(3)
    df.fillna(0, inplace=True)
    # 9点35前后分开，避开开盘情绪不稳定区
    accelerate_grade = 0
    if df.loc[last_index, 'inc_delta_1'] >= 0.8 or df.loc[last_index, 'inc_delta_3'] >= 2:
        delta_1_grade = df.loc[last_index, 'inc_delta_1'] * 10
        delta_3_grade = df.loc[last_index, 'inc_delta_3'] * 5
        accelerate_grade = delta_1_grade if delta_1_grade > delta_3_grade else delta_3_grade
    if time < '09:35:00':
        accelerate_grade *= 1 / 3
    # 快速拉升去除下跌罚分
    if accelerate_grade >= 10 and inc_grade < 0:
        inc_grade = 0
    #加入量比 10
    vr_grade = 0
    volume_rate = df.loc[last_index,'volume_rate']
    if volume_rate < 0.8:
        vr_grade = 0
    elif volume_rate < 1.5:
        vr_grade = 3
    elif volume_rate < 2.5:
        vr_grade = 10
    elif volume_rate < 5:
        vr_grade = 8
    elif volume_rate < 8:
        vr_grade =3
    else:
        vr_grade = 0
    # if time < '09:35:00':
    #加入分时量
    #加入换手率
    #加入换手金额

    #计算趋势（平均值走向，当前价格位次） 30
    trend_grade =0
    if last_index > 20:
        df['mean_shift_5'] = df['mean_5'].shift(5)
        df['mean_shift_30'] = df['mean_5'].shift(30)
        df.fillna(0, inplace=True)
        df['mean_shift_5_delta'] = df['mean_5'] - df['mean_shift_5']
        df['mean_shift_30_delta'] = df['mean_30'] - df['mean_shift_30']
        trend_5 = df.loc[last_index,'mean_shift_5_delta']
        trend_30 = df.loc[last_index,'mean_shift_30_delta']
        #位次
        price_list = df['price'].to_list()
        price_list.sort(reverse=True)
        rank = (price_list.index(df.loc[last_index,'price']) + 1)/(last_index+1)
        #暂时停掉，尚不成熟

        # if rank <= 1/3:
        #     rank_grade = 15 * 2
        # elif rank <= 1/2:
        #     rank_grade= 5 *2
        # else:
        #     rank_grade = 0
        # trend_grade = rank_grade

    #计算低于平均线的值，低于平均线的值大说明负向振荡剧烈 20
    df['mean_delta'] = df['increase'] - df['mean_5']


    grade = (inc_grade + trend_grade +accelerate_grade + vr_grade) * time_line_power
    return grade
'''
increase涨幅控制
涨幅在黄金区域控制不破百，突破黄金区域后，看低股则压低分数，看板股则助力突破100
'''
def inc_control(grade,inc):
    if inc < 2.5:
        if grade >= 90:
            grade = 89.99
    if inc <= 3.5:
        if grade > 100:
            grade = 100
    else:
        grade += (inc - 2.5) * 8
        # if grade >= 90:
        #     grade += (inc - 2.5) * 8
        # else:
        #     grade -= (inc - 2.5) * 8
    return grade
def compute_algo_grade(base_grade,inc,bk_sort,bk_inc,in_sort,time_line_df):
    grade = 0
    ba_grade = base_grade_com(base_grade)
    b_grade = bk_grade(bk_sort,bk_inc,in_sort)
    df = copy.deepcopy(time_line_df)
    tl_grade = time_line_grade(df)
    # grade = ba_grade + b_grade + tl_grade
    # print('縂分：{}， k綫分數：{}, 板塊分數：{}'.format(grade,ba_grade,b_grade))
    grade = tl_grade
    # grade = inc_control(grade, inc)
    return grade
if __name__ == '__main__':
    pass