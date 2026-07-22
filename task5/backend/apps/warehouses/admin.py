from django.contrib import admin

from .models import Warehouse


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "code",
        "name",
        "is_active",
        "latitude",
        "longitude",
        "processing_time_seconds",
        "heavy_fleet_priority",
        "daily_processing_capacity",
        "created_at",
    )

    list_display_links = (
        "id",
        "code",
        "name",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "code",
        "name",
    )

    list_editable = (
        "is_active",
        "processing_time_seconds",
        "heavy_fleet_priority",
        "daily_processing_capacity",
    )

    ordering = (
        "id",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (

        (
            "Basic Information",
            {
                "fields": (
                    "code",
                    "name",
                    "is_active",
                )
            }
        ),

        (
            "Location",
            {
                "fields": (
                    "latitude",
                    "longitude",
                )
            }
        ),

        (
            "Processing Configuration",
            {
                "fields": (
                    "processing_time_seconds",
                    "heavy_fleet_priority",
                    "daily_processing_capacity",
                )
            }
        ),

        (
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            }
        ),

    )