from django.urls import path

from .views import BookingCreateView, MyBookingsView

urlpatterns = [
    path("bookings/", BookingCreateView.as_view(), name="booking-create"),
    path("bookings/my/", MyBookingsView.as_view(), name="bookings-my"),
]

