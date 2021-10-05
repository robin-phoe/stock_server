
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
def base_grade(base_grade):
    grade = 0
    # 基础日K分数
    base_grade_power = 0.8
    if base_grade >= 20000:
        grade = 100
    elif base_grade >= 10000:
        grade = (base_grade - 10000) / 100
    grade = grade * base_grade_power
    return grade
'''
板块分数
'''
def bk_grade():
    pass
'''
大盘分数
'''
def market_grade():
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
def compute_algo_grade(base_grade,inc):
    grade = 0
    grade += base_grade(base_grade)
    grade = inc_control(grade, inc)
    return grade
if __name__ == '__main__':
    pass