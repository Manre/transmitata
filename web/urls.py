"""urls for web"""
from django.urls import path

from .views import HomeView, HomeV2View

app_name = "web"

urlpatterns = [
    path(
        "",
        HomeView.as_view(),
        name="home",
    ),
    path(
        "v2/",
        HomeV2View.as_view(),
        name="home-v2",
    ),
]
