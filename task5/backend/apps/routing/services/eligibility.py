from apps.inventory.models import WarehouseInventory


def get_eligible_warehouses(
    sku_id,
    quantity
):

    inventories = (

        WarehouseInventory.objects

        .select_related(
            "warehouse",
            "sku"
        )

        .filter(

            sku_id=sku_id,
            quantity__gte=quantity
        )

    )

    eligible_warehouses = []
    for inventory in inventories:
        available_quantity = (
            inventory.quantity
            -
            inventory.reserved_quantity

        )

        if (

            available_quantity
            >=
            quantity

        ):

            eligible_warehouses.append(

                {
                    "warehouse":
                    inventory.warehouse,

                    "inventory":
                    inventory,
                    
                    "available_quantity":
                    available_quantity

                }

            )

    return eligible_warehouses