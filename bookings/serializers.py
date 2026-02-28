from rest_framework import serializers

from .models import Booking
from trains.serializers import TrainSerializer


class BookingSerializer(serializers.ModelSerializer):
    train = TrainSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ("id", "train", "seats_booked", "booking_time", "status")


class BookingCreateSerializer(serializers.Serializer):
    train_id = serializers.IntegerField()
    seats = serializers.IntegerField(min_value=1)

