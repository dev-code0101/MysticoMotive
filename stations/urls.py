from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RouteStationViewSet, RouteViewSet, StationViewSet

router = DefaultRouter()
router.register(r"stations", StationViewSet, basename="station")
router.register(r"routes", RouteViewSet, basename="route")
router.register(r"route-stations", RouteStationViewSet, basename="route-station")

urlpatterns = [
    path("", include(router.urls)),
]

