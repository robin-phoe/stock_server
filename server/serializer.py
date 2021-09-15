from rest_framework import serializers

from server.models import StockTradeData,RemenXiaoboxin


class stocksSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTradeData
        # fields = '__all__'
        fields = ["stock_id","trade_date","open_price","close_price",
                  "low_price","high_price","turnover_rate","point_type"]
class stocksSerializer1(serializers.ModelSerializer):
    class Meta:
        model = RemenXiaoboxin
        fields = '__all__'
        # fields = ["stock_id","trade_date","open_price","close_price",
        #           "low_price","high_price","turnover_rate","point_type"]