from django.urls import path, include
from rest_framework.routers import DefaultRouter

from server import views


router = DefaultRouter()
router.register('main', views.stocksViewSet)
router.register('k_line', views.stocksViewSet)

urlpatterns = [
    path('', include(router.urls)),
]