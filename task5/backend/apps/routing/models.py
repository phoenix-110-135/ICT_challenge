from django.db import models


class RoutingRequest(
    models.Model
):

    customer_latitude = models.FloatField()

    customer_longitude = models.FloatField()

    selected_warehouse = models.ForeignKey(

        "warehouses.Warehouse",

        on_delete=models.SET_NULL,

        null=True,

        blank=True,

        related_name="routing_requests"

    )

    estimated_delivery_time = models.FloatField(

        null=True,

        blank=True

    )

    total_cost = models.FloatField(

        null=True,

        blank=True

    )

    route_optimization_score = models.FloatField(

        null=True,

        blank=True

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    class Meta:

        ordering = [

            "-created_at"

        ]

    def __str__(
        self
    ):

        return (

            f"Routing Request "
            f"{self.id}"

        )