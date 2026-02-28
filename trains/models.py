from django.db import models

from stations.models import Route


class Train(models.Model):
    DIRECTION_FORWARD = "FORWARD"
    DIRECTION_BACKWARD = "BACKWARD"

    DIRECTION_CHOICES = (
        (DIRECTION_FORWARD, "Forward"),
        (DIRECTION_BACKWARD, "Backward"),
    )

    train_number = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    route = models.ForeignKey(Route, on_delete=models.PROTECT)
    direction = models.CharField(max_length=8, choices=DIRECTION_CHOICES, default=DIRECTION_FORWARD)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.train_number} – {self.name}"

