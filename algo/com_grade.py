from fractions import Fraction
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
    base_grade_power = 1
    if base_grade >= 20000:
        grade = 100
    elif base_grade >= 10000:
        grade = (base_grade - 10000) / 100
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
    grade += 40

    #内排名 str
    in_sort = Fraction(in_sort)
    mul = float(-1/(in_sort**2) + 1)
    if mul < 0.1:
        mul = 0.1
    grade += grade * mul
    return grade
'''
大盘分数
'''
def market_grade():
    pass
'''
timeline 分数
'''
def time_line_grade():
    pass
'''
increase涨幅控制
涨幅在黄金区域控制不破百，突破黄金区域后，看低股则压低分数，看板股则助力突破100
'''
def inc_control(grade,inc):
    if inc >= 2.5:
        pass
    if inc <= 3.5:
        if grade > 100:
            grade = 100
    else:
        if grade >= 90:
            grade += (inc - 2.5) * 8
        else:
            grade -= (inc - 2.5) * 8
    return grade
def compute_algo_grade(base_grade,inc,bk_sort,bk_inc,in_sort):
    grade = 0
    grade += base_grade_com(base_grade)
    grade += bk_grade(bk_sort,bk_inc,in_sort)
    grade = inc_control(grade, inc)
    return grade
if __name__ == '__main__':
    pass