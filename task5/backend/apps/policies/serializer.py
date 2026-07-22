from rest_framework import serializers

from .models import (
    RoutingPolicy
)


class RoutingPolicySerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = RoutingPolicy

        fields = [
            "id",
            "name",
            "description",
            "cost_weight",
            "time_weight",
            "distance_weight",
            "traffic_weight",
            "is_active",
            "created_at",
            "updated_at",
        ]

    def validate(
        self,
        attrs
    ):

        total_weight = (

            attrs.get(
                "cost_weight",
                self.instance.cost_weight
                if self.instance
                else 0
            )
            +
            attrs.get(
                "time_weight",
                self.instance.time_weight
                if self.instance
                else 0
            )
            +
            attrs.get(
                "distance_weight",
                self.instance.distance_weight
                if self.instance
                else 0
            )
            +
            attrs.get(
                "traffic_weight",
                self.instance.traffic_weight
                if self.instance
                else 0
            )
        )

        if round(
            total_weight,
            5
        ) != 1:

            raise serializers.ValidationError(
                "The sum of the policy weights must be equal to 1."
            )

        return attrs