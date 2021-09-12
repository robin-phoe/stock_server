from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from server.models import stocks
from server.serializer import stocksSerializer


class stocksViewSet(viewsets.ModelViewSet):
    queryset = stocks.objects.all()
    serializer_class = stocksSerializer

class stock_k_line():
    pass