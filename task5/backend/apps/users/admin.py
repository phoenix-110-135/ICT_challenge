from django.contrib import admin
import jdatetime
from .models import User ,PendingRegistration


def jalali_datetime(value):
    if not value:
        return "-"
    value = value.astimezone()
    jalali = jdatetime.datetime.fromgregorian(
        datetime=value
    )
    return jalali.strftime(
        "%Y-%m-%d %H:%M:%S"
    )
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "phone_number",
        "is_verified",
        "created_at_jalali"
    )
    search_fields = (
        "username",
        "phone_number"
    )
    list_filter = (
        "is_verified",
        "is_staff",
        "is_superuser"
    )
    @admin.display(
    )
    def created_at_jalali(
        self,
        obj
    ):
        return jalali_datetime(
            obj.created_at
        )
@admin.register(PendingRegistration)
class PendingRegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "phone_number",
        "otp_code",
        "created_at_jalali"
    )
    search_fields = (
        "username",
        "phone_number"
    )
    ordering = (
        "-created_at",
    )
    @admin.display(
    )
    def created_at_jalali(
        self,
        obj
    ):
        return jalali_datetime(
            obj.created_at
        )
