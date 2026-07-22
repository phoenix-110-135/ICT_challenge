from rest_framework.routers import DefaultRouter
from .views import RoutingPolicyViewSet

router = DefaultRouter()
router.register(
    "routing-policies",
    RoutingPolicyViewSet,
    basename="routing-policy"

)

urlpatterns = (
    router.urls
)