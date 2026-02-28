from rest_framework import permissions, viewsets

from .models import Route, RouteStation, Station
from .serializers import RouteSerializer, RouteStationSerializer, StationSerializer


class IsAdminUser(permissions.IsAdminUser):
    """
    Explicit alias to clarify intention: only admin users can manage stations/routes.
    """


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    permission_classes = [IsAdminUser]


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [IsAdminUser]


class RouteStationViewSet(viewsets.ModelViewSet):
    queryset = RouteStation.objects.select_related("route", "station").all()
    serializer_class = RouteStationSerializer
    permission_classes = [IsAdminUser]

