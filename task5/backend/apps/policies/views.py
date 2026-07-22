from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import RoutingPolicy
from .serializer import RoutingPolicySerializer

class RoutingPolicyViewSet(
    ModelViewSet
):
    queryset = (
        RoutingPolicy.objects.all()
    )
    serializer_class = (
        RoutingPolicySerializer
    )
    permission_classes = [
        IsAuthenticated
    ]