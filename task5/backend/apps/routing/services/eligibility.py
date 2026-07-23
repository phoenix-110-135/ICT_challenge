from django.db.models import F, ExpressionWrapper
from django.db.models import IntegerField

from apps.inventory.models import WarehouseInventory


def get_eligible_inventories(
    order
):

    return (

        WarehouseInventory.objects

        .select_related(

            "warehouse",

            "sku"

        )

        .annotate(

            available_stock=

                ExpressionWrapper(

                    F("quantity")

                    -

                    F("reserved_quantity"),

                    output_field=

                        IntegerField()

                )

        )

        .filter(

            sku=order.sku,

            available_stock__gte=order.quantity,

            warehouse__is_active=True

        )

    )