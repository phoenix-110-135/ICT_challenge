from django.contrib import admin
from .models import RoutingPolicy



@admin.register(
    RoutingPolicy
)
class RoutingPolicyAdmin(
    admin.ModelAdmin
):

    list_display = [
        "name",
        "cost_weight",
        "time_weight",
        "distance_weight",
        "traffic_weight",
        "is_active",
    ]

    list_filter = [
        "is_active",
    ]