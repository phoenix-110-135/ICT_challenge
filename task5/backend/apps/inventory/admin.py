from django.contrib import admin

from .models import (
    SKU,
    WarehouseInventory
)


@admin.register(
    SKU
)
class SKUAdmin(
    admin.ModelAdmin
):

    list_display = [

        "id",
        "code",
        "name",
        "is_active",
        "created_at",

    ]

    search_fields = [

        "code",
        "name",

    ]

    list_filter = [

        "is_active",

    ]


@admin.register(
    WarehouseInventory
)
class WarehouseInventoryAdmin(
    admin.ModelAdmin
):

    list_display = [

        "warehouse",
        "sku",
        "quantity",
        "reserved_quantity",
        "available_quantity",
        "updated_at",

    ]

    search_fields = [

        "warehouse__code",
        "warehouse__name",
        "sku__code",
        "sku__name",

    ]

    list_filter = [

        "warehouse",
        "sku",

    ]

    autocomplete_fields = [

        "warehouse",
        "sku",

    ]

    readonly_fields = [

        "available_quantity",

    ]