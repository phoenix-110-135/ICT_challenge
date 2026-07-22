from rest_framework import serializers

from .models import (
    SKU,
    WarehouseInventory
)


class SKUSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = SKU

        fields = [
            "id",
            "code",
            "name",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class WarehouseInventorySerializer(
    serializers.ModelSerializer
):

    warehouse_code = serializers.CharField(
        source="warehouse.code",
        read_only=True
    )

    sku_code = serializers.CharField(
        source="sku.code",
        read_only=True
    )

    available_quantity = serializers.IntegerField(
        read_only=True
    )

    class Meta:

        model = WarehouseInventory

        fields = [
            "id",
            "warehouse",
            "warehouse_code",
            "sku",
            "sku_code",
            "quantity",
            "reserved_quantity",
            "available_quantity",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "warehouse_code",
            "sku_code",
            "available_quantity",
            "updated_at",
        ]