from rest_framework import serializers

from .models import Route, RouteStation, Station


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ("id", "code", "name", "city", "state")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "name", "description")


class RouteStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteStation
        fields = ("id", "route", "station", "order")

