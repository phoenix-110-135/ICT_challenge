from rest_framework.viewsets import ModelViewSet

from .models import Warehouse
from .serializer import WarehouseSerializer


class WarehouseViewSet(ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer