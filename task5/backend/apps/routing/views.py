from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.warehouses.models import Warehouse
from apps.policies.services import get_active_policy
from .models import RoutingRequest
from .serializers import RoutingRequestSerializer
from .services.optimizer import select_best_warehouse

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
        customer_latitude = (
            request.data.get(
                "customer_latitude"
            )
        )
        customer_longitude = (
            request.data.get(
                "customer_longitude"
            )
        )
        candidates = (
            request.data.get(
                "candidates",
                []
            )
        )

        if not candidates:

            return Response(

                {
                    "error":
                    "No candidate has been submitted for routing."
                },

                status=status.HTTP_400_BAD_REQUEST

            )

        policy = (
            get_active_policy()
        )

        best_warehouse = (
            select_best_warehouse(
                candidates,
                policy
            )
        )

        if not best_warehouse:
            return Response(
                {
                    "error":
                    "No suitable warehouse was found."
                },

                status=status.HTTP_404_NOT_FOUND
            )

        routing_request = (
            RoutingRequest.objects.create(
                customer_latitude=
                customer_latitude,
                customer_longitude=
                customer_longitude,
                selected_warehouse_id=
                best_warehouse[
                    "warehouse_id"
                ],
                estimated_delivery_time=
                best_warehouse[
                    "estimated_time"
                ],

                total_cost=
                best_warehouse[
                    "transportation_cost"
                ],

                route_optimization_score=
                best_warehouse[
                    "route_optimization_score"
                ]

            )

        )

        return Response(

            {
                "warehouse_id":
                best_warehouse[
                    "warehouse_id"
                ],
                "estimated_delivery_time":
                best_warehouse[
                    "estimated_time"
                ],
                "total_cost":
                best_warehouse[
                    "transportation_cost"
                ],
                "route_optimization_score":
                best_warehouse[
                    "route_optimization_score"
                ]
            },
            status=status.HTTP_200_OK
        )