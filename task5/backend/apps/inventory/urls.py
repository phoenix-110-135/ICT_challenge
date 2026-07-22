from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path ,include

router = DefaultRouter()


router.register(
    "skus",
    SKUViewSet,
    basename="sku"
)


router.register(
    "stock",
    WarehouseInventoryViewSet,
    basename="warehouse-stock"
)


urlpatterns = [

    path(
        "",
        include(
            router.urls
        )
    )

]