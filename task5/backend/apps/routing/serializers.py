from rest_framework import serializers


class RouteOptimizationSerializer(
    serializers.Serializer
):

    sku_id = serializers.IntegerField(
        min_value=1
    )

    quantity = serializers.IntegerField(
        min_value=1
    )

    customer_latitude = serializers.DecimalField(
        max_digits=9,
        decimal_places=6
    )

    customer_longitude = serializers.DecimalField(
        max_digits=9,
        decimal_places=6
    )

    def validate_customer_latitude(
        self,
        value
    ):

        if not -90 <= value <= 90:
            raise serializers.ValidationError(
                "Latitude must be between -90 and 90."
            )

        return value

    def validate_customer_longitude(
        self,
        value
    ):

        if not -180 <= value <= 180:
            raise serializers.ValidationError(
                "Longitude must be between -180 and 180."
            )

        return value