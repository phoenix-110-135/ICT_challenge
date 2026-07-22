from django.contrib import admin

from .models import Order


@admin.register(
    Order
)
class OrderAdmin(
    admin.ModelAdmin
):

    list_display = (

        "id",

        "sku",

        "quantity",

        "status",

        "customer_latitude",

        "customer_longitude",

        "created_at"

    )


    list_filter = (

        "status",

        "created_at"

    )


    search_fields = (

        "sku__code",

        "sku__name"

    )