from rest_framework.viewsets import (
    ModelViewSet
)

from rest_framework.permissions import (
    IsAuthenticated
)

from django.db.models import (
    F,
    ExpressionWrapper,
    IntegerField
)

from .models import (
    SKU,
    WarehouseInventory
)

from .serializer import (
    SKUSerializer,
    WarehouseInventorySerializer
)


class SKUViewSet(
    ModelViewSet
):

    queryset = SKU.objects.all()

    serializer_class = (
        SKUSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]


class WarehouseInventoryViewSet(
    ModelViewSet
):

    queryset = (
        WarehouseInventory.objects
        .select_related(
            "warehouse",
            "sku"
        )
    )

    serializer_class = (
        WarehouseInventorySerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(
        self
    ):

        queryset = super().get_queryset()

        warehouse_id = self.request.query_params.get(
            "warehouse"
        )

        sku_id = self.request.query_params.get(
            "sku"
        )

        only_available = self.request.query_params.get(
            "only_available"
        )

        if warehouse_id:

            queryset = queryset.filter(
                warehouse_id=warehouse_id
            )

        if sku_id:

            queryset = queryset.filter(
                sku_id=sku_id
            )

        if only_available == "true":

            queryset = queryset.annotate(

                calculated_available=ExpressionWrapper(

                    F("quantity")
                    -
                    F("reserved_quantity"),

                    output_field=IntegerField()

                )

            ).filter(

                calculated_available__gt=0

            )

        return queryset