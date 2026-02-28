from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Booking
from .serializers import BookingCreateSerializer, BookingSerializer
from trains.models import Train


class BookingCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = BookingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        train_id = serializer.validated_data["train_id"]
        seats = serializer.validated_data["seats"]

        try:
            train = Train.objects.get(id=train_id)
        except Train.DoesNotExist:
            return Response(
                {"detail": "Train not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            booking = Booking.create_with_seat_lock(
                user=request.user,
                train=train,
                seats=seats,
            )
        except ValueError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)


class MyBookingsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = (
            Booking.objects.filter(user=request.user)
            .select_related("train", "train__route")
            .order_by("-booking_time")
        )
        serializer = BookingSerializer(qs, many=True)
        return Response(serializer.data)

