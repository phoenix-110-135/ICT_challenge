from django.db import models


class Warehouse(models.Model):

    code = models.CharField(
        max_length=50,
        unique=True
    )

    name = models.CharField(
        max_length=255
    )

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6
    )

    is_active = models.BooleanField(
        default=True
    )

    processing_time_seconds = models.PositiveIntegerField(
        default=0
    )

    heavy_fleet_priority = models.PositiveIntegerField(
        default=0
    )

    daily_processing_capacity = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.code} - {self.name}"