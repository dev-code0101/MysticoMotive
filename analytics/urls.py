from django.urls import path

from .views import TopRoutesView

urlpatterns = [
    path("top-routes/", TopRoutesView.as_view(), name="analytics-top-routes"),
]

