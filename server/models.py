# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models



class BankuaiDayData(models.Model):
    bk_id = models.CharField(primary_key=True, max_length=45)
    bk_name = models.CharField(max_length=45, blank=True, null=True)
    bk_code = models.CharField(max_length=45, blank=True, null=True)
    trade_date = models.DateTimeField(blank=True, null=True)
    grade = models.FloatField(blank=True, null=True)
    open_price = models.FloatField(blank=True, null=True)
    close_price = models.FloatField(blank=True, null=True)
    high_price = models.FloatField(blank=True, null=True)
    low_price = models.FloatField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    amount_money = models.FloatField(blank=True, null=True)
    zhenfu = models.FloatField(blank=True, null=True)
    increase = models.FloatField(blank=True, null=True)
    turnover_rate = models.FloatField(blank=True, null=True)
    shangzhang_jiashu = models.IntegerField(blank=True, null=True)
    xiadie_jiashu = models.IntegerField(blank=True, null=True)
    lingzhang = models.CharField(max_length=45, blank=True, null=True)
    lingzhang_zhangfu = models.FloatField(blank=True, null=True)
    redu = models.FloatField(blank=True, null=True)
    ranks = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'bankuai_day_data'


class ComZhuang(models.Model):
    stock_id = models.CharField(primary_key=True, max_length=45)
    stock_name = models.CharField(max_length=45, blank=True, null=True)
    zhuang_grade = models.FloatField(blank=True, null=True)
    zhuang_section = models.CharField(max_length=200, blank=True, null=True)
    yidong = models.CharField(max_length=200, blank=True, null=True)
    zhuang_long = models.FloatField(blank=True, null=True)
    max_avg_rate = models.FloatField(blank=True, null=True)
    lasheng_flag = models.FloatField(blank=True, null=True)
    monitor = models.IntegerField(blank=True, null=True)
    reason = models.CharField(max_length=200, blank=True, null=True)
    bk_name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'com_zhuang'


class ComZhuang0427(models.Model):
    stock_id = models.CharField(primary_key=True, max_length=45)
    stock_name = models.CharField(max_length=45, blank=True, null=True)
    zhuang_grade = models.FloatField(blank=True, null=True)
    zhuang_section = models.CharField(max_length=200, blank=True, null=True)
    yidong = models.CharField(max_length=200, blank=True, null=True)
    zhuang_long = models.FloatField(blank=True, null=True)
    max_avg_rate = models.FloatField(blank=True, null=True)
    lasheng_flag = models.FloatField(blank=True, null=True)
    monitor = models.IntegerField(blank=True, null=True)
    reason = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'com_zhuang0427'




class ComputeZhuangTest(models.Model):
    trade_code = models.CharField(primary_key=True, max_length=45)
    stock_id = models.CharField(max_length=45, blank=True, null=True)
    stock_name = models.CharField(max_length=45, blank=True, null=True)
    zhuang_grade = models.FloatField(blank=True, null=True)
    dibu_date = models.DateField(blank=True, null=True)
    huanshouqujian = models.CharField(max_length=200, blank=True, null=True)
    huitiaoqujain = models.CharField(max_length=200, blank=True, null=True)
    lasheng = models.FloatField(blank=True, null=True)
    compute_zhuang_testcol = models.CharField(max_length=45, blank=True, null=True)
    compute_zhuang_testcol1 = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'compute_zhuang_test'





class LimitUpSingle(models.Model):
    trade_code = models.CharField(primary_key=True, max_length=45)
    stock_id = models.CharField(max_length=45, blank=True, null=True)
    stock_name = models.CharField(max_length=45, blank=True, null=True)
    trade_date = models.DateTimeField(blank=True, null=True)
    grade = models.FloatField(blank=True, null=True)
    monitor = models.IntegerField(blank=True, null=True)
    reason = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'limit_up_single'


class LonghuInfo(models.Model):
    trade_code = models.CharField(primary_key=True, max_length=45)
    stock_id = models.CharField(max_length=45, blank=True, null=True)
    stock_name = models.CharField(max_length=45, blank=True, null=True)
    jmmoney = models.FloatField(blank=True, null=True)
    bmoney = models.FloatField(blank=True, null=True)
    smoney = models.FloatField(blank=True, null=True)
    lh_trade_money = models.FloatField(blank=True, null=True)
    all_trade_money = models.FloatField(blank=True, null=True)
    reson = models.CharField(max_length=45, blank=True, null=True)
    jmrate = models.FloatField(blank=True, null=True)
    all_trade_rate = models.FloatField(blank=True, null=True)
    turnover = models.FloatField(blank=True, null=True)
    lt_value = models.FloatField(blank=True, null=True)
    jd = models.CharField(max_length=45, blank=True, null=True)
    trade_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'longhu_info'


class MiuTradeDate(models.Model):
    stock_id = models.CharField(primary_key=True, max_length=45)
    trade_date = models.CharField(max_length=45)
    data = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'miu_trade_date'
        unique_together = (('stock_id', 'trade_date'),)


class Monitor(models.Model):
    trade_code = models.CharField(primary_key=True, max_length=45)
    stock_id = models.CharField(max_length=45, blank=True, null=True)
    trade_date = models.DateTimeField(blank=True, null=True)
    stock_name = models.CharField(max_length=45, blank=True, null=True)
    monitor = models.IntegerField(blank=True, null=True)
    reason = models.CharField(max_length=200, blank=True, null=True)
    monitor_type = models.CharField(max_length=45)
    grade = models.FloatField(blank=True, null=True)
    bk_name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'monitor'
        unique_together = (('trade_code', 'monitor_type'),)


class RemenBoxin(models.Model):
    trade_code = models.CharField(primary_key=True, max_length=45)
    stock_id = models.CharField(max_length=45, blank=True, null=True)
    stock_name = models.CharField(max_length=45, blank=True, null=True)
    trade_date = models.DateField(blank=True, null=True)
    grade = models.FloatField(blank=True, null=True)
    remen_xiaoboxincol = models.CharField(max_length=45, blank=True, null=True)
    monitor = models.IntegerField(blank=True, null=True)
    reason = models.CharField(max_length=200, blank=True, null=True)
    validate_layer = models.IntegerField(blank=True, null=True)
    bk_name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'remen_boxin'


class RemenRetracement(models.Model):
    trade_code = models.CharField(primary_key=True, max_length=45)
    stock_id = models.CharField(max_length=45, blank=True, null=True)
    stock_name = models.CharField(max_length=45, blank=True, null=True)
    trade_date = models.DateField(blank=True, null=True)
    grade = models.FloatField(blank=True, null=True)
    remen_xiaoboxincol = models.CharField(max_length=45, blank=True, null=True)
    monitor = models.IntegerField(blank=True, null=True)
    reason = models.CharField(max_length=200, blank=True, null=True)
    validate_layer = models.IntegerField(blank=True, null=True)
    bk_name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'remen_retracement'


class RemenXiaoboxin(models.Model):
    trade_code = models.CharField(primary_key=True, max_length=45)
    stock_id = models.CharField(max_length=45, blank=True, null=True)
    stock_name = models.CharField(max_length=45, blank=True, null=True)
    trade_date = models.DateField(blank=True, null=True)
    grade = models.FloatField(blank=True, null=True)
    remen_xiaoboxincol = models.CharField(max_length=45, blank=True, null=True)
    monitor = models.IntegerField(blank=True, null=True)
    reason = models.CharField(max_length=200, blank=True, null=True)
    validate_layer = models.IntegerField(blank=True, null=True)
    bk_name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'remen_xiaoboxin'


class RemenXiaoboxinC(models.Model):
    trade_code = models.CharField(primary_key=True, max_length=45)
    stock_id = models.CharField(max_length=45, blank=True, null=True)
    stock_name = models.CharField(max_length=45, blank=True, null=True)
    trade_date = models.DateField(blank=True, null=True)
    grade = models.FloatField(blank=True, null=True)
    remen_xiaoboxincol = models.CharField(max_length=45, blank=True, null=True)
    monitor = models.IntegerField(blank=True, null=True)
    reason = models.CharField(max_length=200, blank=True, null=True)
    validate_layer = models.IntegerField(blank=True, null=True)
    bk_name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'remen_xiaoboxin_c'









# class StockInformations(models.Model):
#     stock_name = models.CharField(max_length=45)
#     stock_id = models.CharField(primary_key=True, max_length=45)
#     ������ = models.FloatField(blank=True, null=True)
#     bk_name = models.CharField(max_length=45, blank=True, null=True)
#     ֤�����ҵ = models.CharField(max_length=45, blank=True, null=True)
#     business = models.CharField(max_length=45, blank=True, null=True)
#     main_business = models.CharField(max_length=500, blank=True, null=True)
#     related = models.CharField(max_length=500, blank=True, null=True)
#     h_table = models.CharField(max_length=45, blank=True, null=True)
#     exchange = models.CharField(max_length=45, blank=True, null=True)
#     �������� = models.DateField(blank=True, null=True)
#     ������ = models.CharField(max_length=250, blank=True, null=True)
#     ÿ�ɷ��м� = models.CharField(max_length=45, blank=True, null=True)
#     ���� = models.CharField(max_length=45, blank=True, null=True)
#     ��Ա���� = models.CharField(max_length=45, blank=True, null=True)
#     ��˾��� = models.TextField(blank=True, null=True)
#     ��Ӫ��Χ = models.CharField(max_length=1500, blank=True, null=True)
#     bk_code = models.CharField(max_length=45, blank=True, null=True)
#     stock_informationscol1 = models.CharField(max_length=45, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'stock_informations'


class StockTradeData(models.Model):
    trade_code = models.CharField(primary_key=True, max_length=20)
    stock_name = models.CharField(max_length=45, blank=True, null=True)
    stock_id = models.CharField(max_length=45, blank=True, null=True)
    trade_date = models.DateTimeField(blank=True, null=True)
    open_price = models.FloatField(blank=True, null=True)
    close_price = models.FloatField(blank=True, null=True)
    high_price = models.FloatField(blank=True, null=True)
    low_price = models.FloatField(blank=True, null=True)
    increase = models.FloatField(blank=True, null=True)
    turnover_rate = models.FloatField(blank=True, null=True)
    trade_amount = models.FloatField(blank=True, null=True)
    trade_money = models.FloatField(blank=True, null=True)
    capital_stock = models.CharField(max_length=45, blank=True, null=True)
    circulation = models.CharField(max_length=45, blank=True, null=True)
    fxl = models.CharField(max_length=45, blank=True, null=True)
    p_e = models.CharField(db_column='P_E', max_length=45, blank=True, null=True)  # Field name made lowercase.
    p_b = models.CharField(db_column='P_B', max_length=45, blank=True, null=True)  # Field name made lowercase.
    # 达标换手率 = models.IntegerField(blank=True, null=True)
    bk_name = models.CharField(max_length=45, blank=True, null=True)
    wave_data = models.FloatField(blank=True, null=True)
    point_type = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'stock_trade_data'




