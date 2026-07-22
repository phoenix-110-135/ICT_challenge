from rest_framework import serializers

from .models import Order


class OrderSerializer(
    serializers.ModelSerializer
):

    sku_code = serializers.CharField(

        source="sku.code",

        read_only=True

    )


    class Meta:

        model = Order

        fields = [

            "id",

            "sku",

            "sku_code",

            "quantity",

            "customer_latitude",

            "customer_longitude",

            "status",

            "created_at",

            "updated_at"

        ]

        read_only_fields = [

            "id",

            "sku_code",

            "status",

            "created_at",

            "updated_at"

        ]