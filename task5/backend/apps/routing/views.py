from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    RouteOptimizationSerializer
)

from .services.optimizer import (
    RouteOptimizer
)


class RouteOptimizationView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def post(
        self,
        request
    ):

        serializer = (
            RouteOptimizationSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        optimizer = (
            RouteOptimizer()
        )

        try:

            result = optimizer.optimize(
                sku_id=serializer.validated_data[
                    "sku_id"
                ],

                quantity=serializer.validated_data[
                    "quantity"
                ],

                customer_latitude=(
                    serializer.validated_data[
                        "customer_latitude"
                    ]
                ),

                customer_longitude=(
                    serializer.validated_data[
                        "customer_longitude"
                    ]
                ),
            )

        except ValueError as error:

            return Response(
                {
                    "detail": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            result,
            status=status.HTTP_200_OK
        )