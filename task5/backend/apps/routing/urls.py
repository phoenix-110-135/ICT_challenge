from django.urls import path

from .views import (
    RouteOptimizationView
)


urlpatterns = [

    path(
        "optimize/",
        RouteOptimizationView.as_view(),
        name="route-optimize"
    ),

]