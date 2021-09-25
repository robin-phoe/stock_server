from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from django.http import HttpResponse,JsonResponse
from server.models import StockTradeData
from server.models import RemenXiaoboxin
from server.serializer import stocksSerializer
from server.serializer import stocksSerializer1

from . import util


# class stocksViewSet(viewsets.ModelViewSet):
#     # pass
#     queryset = RemenXiaoboxin.objects.all()
#     serializer_class = stocksSerializer1

#日k_line
def stock_k_line(request):
    response_json = util.get_kline(request)
    return JsonResponse(response_json)

#分时
def stock_time_line(request):
    response_json = util.time_line(request)
    return JsonResponse(response_json)

#板块k_line
def bk_k_line(request):
    response_json = util.get_bk_kline(request)
    return JsonResponse(response_json)

#板块分时
def bk_time_line(request):
    response_json = util.bk_time_line(request)
    return JsonResponse(response_json)

#algo_monitor
def algo_monitor(request):
    response_json = util.get_algo(request)
    return JsonResponse(response_json)

#取全日algo 分数
def grade_all_day(request):
    response_json = util.get_grade_all_day(request)
    return JsonResponse(response_json)