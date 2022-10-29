"""urls for api"""
from django.urls import path

from .views import RoutesView, FindRoutesView, FindStationsForRoute

urlpatterns = [
    path('route/<str:route_name>', RoutesView.as_view(), name='routes'),
    path('route/<str:route_name>/find', FindRoutesView.as_view(), name='find-routes'),
    path('stations/<str:route_id>/find', FindStationsForRoute.as_view(), name='find-stations'),
]
