from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User ,PendingRegistration 
from .services import generate_otp
from .services import send_sms
from rest_framework.permissions import AllowAny , IsAuthenticated
from datetime import timedelta
from django.utils import timezone
from drf_spectacular.utils import extend_schema
import jdatetime

ACCESS_COOKIE_NAME = "access_token"
REFRESH_COOKIE_NAME = "refresh_token"

def set_auth_cookies(
    response,
    access_token,
    refresh_token
):
    response.set_cookie(
        key=ACCESS_COOKIE_NAME,
        value=str(
            access_token
        ),
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=60 * 15
    )

    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=str(
            refresh_token
        ),
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=60 * 60 * 24 * 7
    )
    return response

####################   register    ##################
@extend_schema(
    summary="Register a new user",
    description=(
        "Starts the user registration process. "
        "After successful registration, an OTP code is sent "
        "to the provided phone number."
    ),
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "username": {
                    "type": "string",
                    "example": "ali",
                    "description": "Unique username"
                },
                "phone_number": {
                    "type": "string",
                    "example": "09123456789",
                    "description": "User phone number"
                },
                "password": {
                    "type": "string",
                    "format": "password",
                    "example": "StrongPassword123",
                    "description": "User password"
                }
            },
            "required": [
                "username",
                "phone_number",
                "password"
            ]
        }
    },
    responses={
        200: {
            "description": "OTP sent successfully"
        },
        400: {
            "description": "Invalid or duplicate user data"
        },
        429: {
            "description": "Too many OTP requests"
        }
    }
)
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get("username")
    phone_number = request.data.get("phone_number")
    password = request.data.get("password")

    if not username or not phone_number or not password:
        return Response(
        {
            "error": (
                "username, phone_number "
                "and password are required"
            )
        },
        status=400
    )


    if User.objects.filter(
        username=username
        ).exists():
        return Response(
        {
            "error": "this username is already registered"
        },
        status=400
    )


    if User.objects.filter(
        phone_number=phone_number
        ).exists():
        return Response(
        {
            "error": "this phone number is already registered"
        },
        status=400
    )


    pending = PendingRegistration.objects.filter(
        phone_number=phone_number
    ).first()

    if pending:
        if timezone.now() - pending.created_at < timedelta(
            minutes=2
        ):
            return Response(
                {
                    "error": (
                        "Please wait 2 minutes "
                        "before requesting another code"
                    )
                },
                status=429
            )


        pending.username = username
        pending.password = make_password(
            password
        )

        pending.otp_code = generate_otp()
        pending.created_at = timezone.now()
        pending.save()


        send_sms(
            phone_number,
            pending.otp_code
        )


        return Response(
            {
                "message": "otp sent"
            },
            status=200
        )


    otp = generate_otp()
    PendingRegistration.objects.create(
        phone_number=phone_number,
        username=username,
        password=make_password(
            password
        ),
        otp_code=otp
    )


    send_sms(
        phone_number,
        otp
    )


    return Response(
        {
            "message": "otp sent"
        },
        status=200
    )




################   verify_otp   ###########
@extend_schema(
    summary="Verify registration OTP",
    description=(
        "Verifies the OTP code sent to the user's phone number. "
        "If the OTP is valid, the user account is created "
        "and authentication cookies are set."
    ),
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "phone_number": {
                    "type": "string",
                    "example": "09123456789"
                },
                "otp": {
                    "type": "string",
                    "example": "123456",
                    "description": "Six-digit OTP code"
                }
            },
            "required": [
                "phone_number",
                "otp"
            ]
        }
    },
    responses={
        201: {
            "description": "Registration successful"
        },
        400: {
            "description": "Invalid or expired OTP"
        }
    }
)
@api_view(["POST"])
@permission_classes([AllowAny])
def verify_otp(request):
    phone_number = request.data.get(
        "phone_number"
    )

    otp = request.data.get(
        "otp"
    )


    pending = PendingRegistration.objects.filter(
        phone_number=phone_number,
        otp_code=otp

    ).first()

    if not pending:

        return Response(
        {
            "error": "invalid otp"
        },
        status=400
    )


    if timezone.now() - pending.created_at > timedelta(

        minutes=2
    ):

        return Response(
        {
            "error": "otp expired"
        },
        status=400
    )


    user = User.objects.create(
        username=pending.username,
        phone_number=pending.phone_number,
        is_verified=True,
        last_login=timezone.now()
    )


    user.password = pending.password

    user.save()


    pending.delete()


    refresh = RefreshToken.for_user(
        user
    )


    response = Response(
        {
            "message": "registration successful"
        },
        status=201
    )


    return set_auth_cookies(
        response,
        refresh.access_token,
        refresh
    )

##############   login  ###############
@extend_schema(
    summary="User login",
    description=(
        "Authenticates the user using either username or phone number. "
        "After successful authentication, access and refresh tokens "
        "are stored in HTTPOnly cookies."
    ),
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "identifier": {
                    "type": "string",
                    "example": "ali",
                    "description": (
                        "Username or phone number"
                    )
                },
                "password": {
                    "type": "string",
                    "format": "password",
                    "example": "StrongPassword123"
                }
            },
            "required": [
                "identifier",
                "password"
            ]
        }
    },
    responses={
        200: {
            "description": "Login successful"
        },
        400: {
            "description": "Invalid credentials"
        },
        403: {
            "description": "User is not verified"
        }
    }
)
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    identifier = request.data.get(
        "identifier"
    )

    password = request.data.get(
        "password"
    )


    user = authenticate(
        username=identifier,
        password=password
    )


    if not user:
        obj = User.objects.filter(
            phone_number=identifier

        ).first()

        if obj:
            user = authenticate(
                username=obj.username,
                password=password
            )


    if not user:
        return Response(
            {
                "error": "invalid credentials"
            },
            status=400
        )


    if not user.is_verified:

        return Response(
            {
                "error": "user is not verified"
            },

            status=403

        )


    user.last_login = timezone.now()


    user.save(
        update_fields=[
            "last_login"
        ]

    )


    refresh = RefreshToken.for_user(
        user
    )


    response = Response(

        {
            "message": "login successful"
        }

    )


    return set_auth_cookies(
        response,
        refresh.access_token,
        refresh
    )

############    profile   ############
@extend_schema(
    summary="Get current user profile",
    description=(
        "Returns information about the currently authenticated user. "
        "Authentication is performed using the HTTPOnly access cookie."
    ),
    responses={
        200: {
            "description": "User profile returned successfully"
        },
        401: {
            "description": "Authentication credentials were not provided"
        }
    }
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user
    return Response(

        {
            "id": user.id,
            "username": user.username,
            "phone_number": user.phone_number,
            "is_verified": user.is_verified,
            "created_at": user.created_at
        }

    )

#########   resend_otp   #########
@extend_schema(
    summary="Resend registration OTP",
    description=(
        "Generates and sends a new OTP code to the phone number "
        "associated with a pending registration."
    ),
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "phone_number": {
                    "type": "string",
                    "example": "09123456789",
                    "description": (
                        "Phone number used during registration"
                    )
                }
            },
            "required": [
                "phone_number"
            ]
        }
    },
    responses={
        200: {
            "description": "New OTP sent successfully"
        },
        404: {
            "description": "No pending registration found"
        },
        429: {
            "description": "Too many requests"
        },
        202: {
            "description": "OTP generated but SMS delivery failed"
        }
    }
)
@api_view(["POST"])
@permission_classes([AllowAny])
def resend_otp(request):

    phone_number = request.data.get(
        "phone_number"
    )


    pending = PendingRegistration.objects.filter(
        phone_number=phone_number
    ).first()

    if not pending:
        return Response(
            {
                "error": "no registration found"
            },
            status=404
        )


    if timezone.now() - pending.created_at < timedelta(
        minutes=2
    ):

        return Response(

            {
                "error": (
                    "Please wait 2 minutes "
                    "before requesting another code"
                )
            },
            status=429
        )


    otp = generate_otp()
    pending.otp_code = otp
    pending.created_at = timezone.now()
    pending.save()
    
    result = send_sms(
        phone_number,
        otp
    )


    if result is None:
        return Response(
            {
                "message": (
                    "Code generated but SMS delivery failed. "
                    "Please try again."
                )
            },

            status=202
        )


    return Response(
        {
            "message": "new code sent"
        }
    )

###########  logout   ############
@extend_schema(
    summary="Logout user",
    description=(
        "Deletes the access and refresh authentication cookies "
        "from the client."
    ),
    responses={
        200: {
            "description": "Logout successful"
        }
    }
)
@api_view(["POST"])
@permission_classes([AllowAny])
def logout(request):
    response = Response(
        {
            "message": "logout successful"
        }
    )
    response.delete_cookie(
        "access_token"
    )
    response.delete_cookie(
        "refresh_token"
    )

    return response
