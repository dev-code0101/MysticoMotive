from django.urls import path

from .views import TrainAdminView, TrainSearchView

urlpatterns = [
    path("trains/", TrainAdminView.as_view(), name="trains-admin"),
    path("trains/search/", TrainSearchView.as_view(), name="trains-search"),
]

