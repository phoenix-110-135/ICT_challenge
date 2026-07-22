from django.db import models

from apps.warehouses.models import Warehouse


class SKU(
    models.Model
):

    code = models.CharField(
        max_length=100,
        unique=True
    )

    name = models.CharField(
        max_length=255
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
            "id"
        ]

    def __str__(
        self
    ):

        return (
            f"{self.code} - "
            f"{self.name}"
        )


class WarehouseInventory(
    models.Model
):

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name="inventories"
    )

    sku = models.ForeignKey(
        SKU,
        on_delete=models.CASCADE,
        related_name="warehouse_inventories"
    )

    quantity = models.PositiveIntegerField(
        default=0
    )

    reserved_quantity = models.PositiveIntegerField(
        default=0
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = [
            "id"
        ]

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "warehouse",
                    "sku"
                ],
                name=(
                    "unique_warehouse_sku"
                )
            )

        ]

    def __str__(
        self
    ):

        return (
            f"{self.warehouse.code} - "
            f"{self.sku.code}"
        )

    @property
    def available_quantity(
        self
    ):

        return max(
            self.quantity
            -
            self.reserved_quantity,

            0
        )

    def has_stock(
        self,
        required_quantity
    ):

        return (
            self.available_quantity
            >=
            required_quantity
        )