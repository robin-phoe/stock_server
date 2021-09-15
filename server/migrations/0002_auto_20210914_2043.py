# Generated by Django 3.1.7 on 2021-09-14 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComputeZhuangTest',
            fields=[
                ('trade_code', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('stock_id', models.CharField(blank=True, max_length=45, null=True)),
                ('stock_name', models.CharField(blank=True, max_length=45, null=True)),
                ('zhuang_grade', models.FloatField(blank=True, null=True)),
                ('dibu_date', models.DateField(blank=True, null=True)),
                ('huanshouqujian', models.CharField(blank=True, max_length=200, null=True)),
                ('huitiaoqujain', models.CharField(blank=True, max_length=200, null=True)),
                ('lasheng', models.FloatField(blank=True, null=True)),
                ('compute_zhuang_testcol', models.CharField(blank=True, max_length=45, null=True)),
                ('compute_zhuang_testcol1', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'compute_zhuang_test',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ComZhuang',
            fields=[
                ('stock_id', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('stock_name', models.CharField(blank=True, max_length=45, null=True)),
                ('zhuang_grade', models.FloatField(blank=True, null=True)),
                ('zhuang_section', models.CharField(blank=True, max_length=200, null=True)),
                ('yidong', models.CharField(blank=True, max_length=200, null=True)),
                ('zhuang_long', models.FloatField(blank=True, null=True)),
                ('max_avg_rate', models.FloatField(blank=True, null=True)),
                ('lasheng_flag', models.FloatField(blank=True, null=True)),
                ('monitor', models.IntegerField(blank=True, null=True)),
                ('reason', models.CharField(blank=True, max_length=200, null=True)),
                ('bk_name', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'com_zhuang',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ComZhuang0427',
            fields=[
                ('stock_id', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('stock_name', models.CharField(blank=True, max_length=45, null=True)),
                ('zhuang_grade', models.FloatField(blank=True, null=True)),
                ('zhuang_section', models.CharField(blank=True, max_length=200, null=True)),
                ('yidong', models.CharField(blank=True, max_length=200, null=True)),
                ('zhuang_long', models.FloatField(blank=True, null=True)),
                ('max_avg_rate', models.FloatField(blank=True, null=True)),
                ('lasheng_flag', models.FloatField(blank=True, null=True)),
                ('monitor', models.IntegerField(blank=True, null=True)),
                ('reason', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'db_table': 'com_zhuang0427',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BankuaiDayData',
            fields=[
                ('bk_id', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('bk_name', models.CharField(blank=True, max_length=45, null=True)),
                ('bk_code', models.CharField(blank=True, max_length=45, null=True)),
                ('trade_date', models.DateTimeField(blank=True, null=True)),
                ('grade', models.FloatField(blank=True, null=True)),
                ('open_price', models.FloatField(blank=True, null=True)),
                ('close_price', models.FloatField(blank=True, null=True)),
                ('high_price', models.FloatField(blank=True, null=True)),
                ('low_price', models.FloatField(blank=True, null=True)),
                ('amount', models.FloatField(blank=True, null=True)),
                ('amount_money', models.FloatField(blank=True, null=True)),
                ('zhenfu', models.FloatField(blank=True, null=True)),
                ('increase', models.FloatField(blank=True, null=True)),
                ('turnover_rate', models.FloatField(blank=True, null=True)),
                ('shangzhang_jiashu', models.IntegerField(blank=True, null=True)),
                ('xiadie_jiashu', models.IntegerField(blank=True, null=True)),
                ('lingzhang', models.CharField(blank=True, max_length=45, null=True)),
                ('lingzhang_zhangfu', models.FloatField(blank=True, null=True)),
                ('redu', models.FloatField(blank=True, null=True)),
                ('ranks', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'bankuai_day_data',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='LimitUpSingle',
            fields=[
                ('trade_code', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('stock_id', models.CharField(blank=True, max_length=45, null=True)),
                ('stock_name', models.CharField(blank=True, max_length=45, null=True)),
                ('trade_date', models.DateTimeField(blank=True, null=True)),
                ('grade', models.FloatField(blank=True, null=True)),
                ('monitor', models.IntegerField(blank=True, null=True)),
                ('reason', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'limit_up_single',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='LonghuInfo',
            fields=[
                ('trade_code', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('stock_id', models.CharField(blank=True, max_length=45, null=True)),
                ('stock_name', models.CharField(blank=True, max_length=45, null=True)),
                ('jmmoney', models.FloatField(blank=True, null=True)),
                ('bmoney', models.FloatField(blank=True, null=True)),
                ('smoney', models.FloatField(blank=True, null=True)),
                ('lh_trade_money', models.FloatField(blank=True, null=True)),
                ('all_trade_money', models.FloatField(blank=True, null=True)),
                ('reson', models.CharField(blank=True, max_length=45, null=True)),
                ('jmrate', models.FloatField(blank=True, null=True)),
                ('all_trade_rate', models.FloatField(blank=True, null=True)),
                ('turnover', models.FloatField(blank=True, null=True)),
                ('lt_value', models.FloatField(blank=True, null=True)),
                ('jd', models.CharField(blank=True, max_length=45, null=True)),
                ('trade_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'longhu_info',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='MiuTradeDate',
            fields=[
                ('stock_id', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('trade_date', models.CharField(max_length=45)),
                ('data', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'miu_trade_date',
                'managed': True,
                'unique_together': {('stock_id', 'trade_date')},
            },
        ),
        migrations.CreateModel(
            name='Monitor',
            fields=[
                ('trade_code', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('stock_id', models.CharField(blank=True, max_length=45, null=True)),
                ('trade_date', models.DateTimeField(blank=True, null=True)),
                ('stock_name', models.CharField(blank=True, max_length=45, null=True)),
                ('monitor', models.IntegerField(blank=True, null=True)),
                ('reason', models.CharField(blank=True, max_length=200, null=True)),
                ('monitor_type', models.CharField(max_length=45)),
                ('grade', models.FloatField(blank=True, null=True)),
                ('bk_name', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'monitor',
                'managed': True,
                'unique_together': {('trade_code', 'monitor_type')},
            },
        ),
        migrations.CreateModel(
            name='RemenBoxin',
            fields=[
                ('trade_code', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('stock_id', models.CharField(blank=True, max_length=45, null=True)),
                ('stock_name', models.CharField(blank=True, max_length=45, null=True)),
                ('trade_date', models.DateField(blank=True, null=True)),
                ('grade', models.FloatField(blank=True, null=True)),
                ('remen_xiaoboxincol', models.CharField(blank=True, max_length=45, null=True)),
                ('monitor', models.IntegerField(blank=True, null=True)),
                ('reason', models.CharField(blank=True, max_length=200, null=True)),
                ('validate_layer', models.IntegerField(blank=True, null=True)),
                ('bk_name', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'remen_boxin',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='RemenRetracement',
            fields=[
                ('trade_code', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('stock_id', models.CharField(blank=True, max_length=45, null=True)),
                ('stock_name', models.CharField(blank=True, max_length=45, null=True)),
                ('trade_date', models.DateField(blank=True, null=True)),
                ('grade', models.FloatField(blank=True, null=True)),
                ('remen_xiaoboxincol', models.CharField(blank=True, max_length=45, null=True)),
                ('monitor', models.IntegerField(blank=True, null=True)),
                ('reason', models.CharField(blank=True, max_length=200, null=True)),
                ('validate_layer', models.IntegerField(blank=True, null=True)),
                ('bk_name', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'remen_retracement',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='RemenXiaoboxin',
            fields=[
                ('trade_code', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('stock_id', models.CharField(blank=True, max_length=45, null=True)),
                ('stock_name', models.CharField(blank=True, max_length=45, null=True)),
                ('trade_date', models.DateField(blank=True, null=True)),
                ('grade', models.FloatField(blank=True, null=True)),
                ('remen_xiaoboxincol', models.CharField(blank=True, max_length=45, null=True)),
                ('monitor', models.IntegerField(blank=True, null=True)),
                ('reason', models.CharField(blank=True, max_length=200, null=True)),
                ('validate_layer', models.IntegerField(blank=True, null=True)),
                ('bk_name', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'remen_xiaoboxin',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='RemenXiaoboxinC',
            fields=[
                ('trade_code', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('stock_id', models.CharField(blank=True, max_length=45, null=True)),
                ('stock_name', models.CharField(blank=True, max_length=45, null=True)),
                ('trade_date', models.DateField(blank=True, null=True)),
                ('grade', models.FloatField(blank=True, null=True)),
                ('remen_xiaoboxincol', models.CharField(blank=True, max_length=45, null=True)),
                ('monitor', models.IntegerField(blank=True, null=True)),
                ('reason', models.CharField(blank=True, max_length=200, null=True)),
                ('validate_layer', models.IntegerField(blank=True, null=True)),
                ('bk_name', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'remen_xiaoboxin_c',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StockTradeData',
            fields=[
                ('trade_code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('stock_name', models.CharField(blank=True, max_length=45, null=True)),
                ('stock_id', models.CharField(blank=True, max_length=45, null=True)),
                ('trade_date', models.DateTimeField(blank=True, null=True)),
                ('open_price', models.FloatField(blank=True, null=True)),
                ('close_price', models.FloatField(blank=True, null=True)),
                ('high_price', models.FloatField(blank=True, null=True)),
                ('low_price', models.FloatField(blank=True, null=True)),
                ('increase', models.FloatField(blank=True, null=True)),
                ('turnover_rate', models.FloatField(blank=True, null=True)),
                ('trade_amount', models.FloatField(blank=True, null=True)),
                ('trade_money', models.FloatField(blank=True, null=True)),
                ('capital_stock', models.CharField(blank=True, max_length=45, null=True)),
                ('circulation', models.CharField(blank=True, max_length=45, null=True)),
                ('fxl', models.CharField(blank=True, max_length=45, null=True)),
                ('p_e', models.CharField(blank=True, db_column='P_E', max_length=45, null=True)),
                ('p_b', models.CharField(blank=True, db_column='P_B', max_length=45, null=True)),
                ('达标换手率', models.IntegerField(blank=True, null=True)),
                ('bk_name', models.CharField(blank=True, max_length=45, null=True)),
                ('wave_data', models.FloatField(blank=True, null=True)),
                ('point_type', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'stock_trade_data',
                'managed': True,
            },
        ),
        migrations.DeleteModel(
            name='stocks',
        ),
    ]
