from django.db import models


class RoutingPolicy(
    models.Model
):

    name = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True
    )

    cost_weight = models.FloatField(
        default=0.4
    )

    time_weight = models.FloatField(
        default=0.3
    )

    distance_weight = models.FloatField(
        default=0.2
    )

    traffic_weight = models.FloatField(
        default=0.1
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = [
            "-created_at"
        ]

    def __str__(
        self
    ):

        return self.name