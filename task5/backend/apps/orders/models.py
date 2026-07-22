from django.db import models
from apps.inventory.models import SKU


class Order(
    models.Model
):

    class Status(
        models.TextChoices
    ):

        PENDING = (
            "pending",
            "Pending"
        )

        PROCESSING = (
            "processing",
            "Processing"
        )

        COMPLETED = (
            "completed",
            "Completed"
        )

        CANCELLED = (
            "cancelled",
            "Cancelled"
        )


    sku = models.ForeignKey(

        SKU,

        on_delete=models.PROTECT,

        related_name="orders"

    )


    quantity = models.PositiveIntegerField()


    customer_latitude = models.DecimalField(

        max_digits=9,

        decimal_places=6

    )


    customer_longitude = models.DecimalField(

        max_digits=9,

        decimal_places=6

    )


    status = models.CharField(

        max_length=20,

        choices=Status.choices,

        default=Status.PENDING

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

        return (

            f"Order #{self.id} - "

            f"{self.sku.code}"

        )