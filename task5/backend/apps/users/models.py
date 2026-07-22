from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    username = models.CharField(
        max_length=50,
        unique=True
    )

    phone_number = models.CharField(
        max_length=15,
        unique=True
    )

    is_verified = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return self.username


class PendingRegistration(models.Model):

    username = models.CharField(
        max_length=50
    )

    phone_number = models.CharField(
        max_length=15,
        unique=True
    )

    password = models.CharField(
        max_length=255
    )

    otp_code = models.CharField(
        max_length=6
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = [
            "-created_at"
        ]

    def __str__(self):

        return self.phone_number
    

