from rest_framework.viewsets import (
    ModelViewSet
)

from rest_framework.permissions import (
    IsAuthenticated
)

from .models import Order

from .serializers import (
    OrderSerializer
)


class OrderViewSet(
    ModelViewSet
):

    queryset = (

        Order.objects

        .select_related(

            "sku"

        )

    )


    serializer_class = (

        OrderSerializer

    )


    permission_classes = [

        IsAuthenticated

    ]