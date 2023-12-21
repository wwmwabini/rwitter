from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="tweets-home"),
    path("search/", views.searchresults, name="tweets-searchresults")
]