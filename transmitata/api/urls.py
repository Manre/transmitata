"""urls for api"""
from django.urls import path

from .views import RoutesView

urlpatterns = [
    path('route/<str:route_name>', RoutesView.as_view(), name='routes')
]
