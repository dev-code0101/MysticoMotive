from rest_framework import serializers

from .models import Train
from .utils import get_station_sequence


class TrainSerializer(serializers.ModelSerializer):
    stations = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Train
        fields = (
            "id",
            "train_number",
            "name",
            "route",
            "direction",
            "departure_time",
            "arrival_time",
            "total_seats",
            "available_seats",
            "stations",
        )

    def get_stations(self, obj: Train):
        return get_station_sequence(obj)

