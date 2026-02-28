from django.db import models


class Station(models.Model):
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.code} – {self.name}"


class Route(models.Model):
    name = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name or f"Route {self.id}"


class RouteStation(models.Model):
    route = models.ForeignKey(Route, related_name="stations", on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        unique_together = ("route", "order")
        ordering = ["order"]

    def __str__(self) -> str:
        return f"{self.route} – {self.station.code} ({self.order})"

