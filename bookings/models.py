from django.db import models, transaction

from trains.models import Train
from users.models import User


class Booking(models.Model):
    STATUS_CONFIRMED = "CONFIRMED"
    STATUS_CANCELED = "CANCELED"

    STATUS_CHOICES = (
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELED, "Canceled"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name="bookings")
    seats_booked = models.PositiveIntegerField()
    booking_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_CONFIRMED)

    def __str__(self) -> str:
        return f"Booking {self.id} – {self.user.email} – {self.train.train_number}"

    @classmethod
    @transaction.atomic
    def create_with_seat_lock(cls, *, user: User, train: Train, seats: int) -> "Booking":
        locked_train = Train.objects.select_for_update().get(pk=train.pk)
        if locked_train.available_seats < seats:
            raise ValueError("Not enough seats")
        locked_train.available_seats -= seats
        locked_train.save(update_fields=["available_seats"])
        booking = cls.objects.create(
            user=user,
            train=locked_train,
            seats_booked=seats,
            status=cls.STATUS_CONFIRMED,
        )
        return booking

