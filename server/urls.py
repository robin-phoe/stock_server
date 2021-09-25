from django.urls import path, include
from rest_framework.routers import DefaultRouter

from server import views

router = DefaultRouter()
# router.register('k', views.stocksViewSet)
# router.register('k', views.stock_k_line)
urlpatterns = [
    path('', include(router.urls)),
    path('k_line', views.stock_k_line),
    path('time_line', views.stock_time_line),
    path('bk_k_line', views.bk_k_line),
    path('bk_time_line', views.bk_time_line),
    path('monitor/algo_monitor', views.algo_monitor),
    path('monitor/grade_all_day', views.grade_all_day),
]