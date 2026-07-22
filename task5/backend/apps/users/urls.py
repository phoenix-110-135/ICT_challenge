from django.urls import path
from .views import *

urlpatterns = [

    path("register/",register,name="register"),
    path("verify-otp/",verify_otp,name="verify-otp"),
    path("resend-otp/",resend_otp,name="resend-otp"),
    path("login/",login,name="login"),
    path("logout/",logout,name="logout"),
    path("profile/",profile,name="profile"),
    path("refresh/",refresh_access_token,name="refresh"),
]
