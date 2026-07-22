from rest_framework import serializers
from .models import RoutingRequest



class RoutingRequestSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = RoutingRequest
        fields = [
            "id",
            "customer_latitude",
            "customer_longitude",
            "selected_warehouse",
            "estimated_delivery_time",
            "total_cost",
            "route_optimization_score",
            "created_at",
        ]
        read_only_fields = [
            "selected_warehouse",
            "estimated_delivery_time",
            "total_cost",
            "route_optimization_score",
            "created_at",
        ]