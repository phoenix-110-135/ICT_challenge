from math import radians, sin, cos, sqrt, atan2

from apps.inventory.models import Warehouse ,WarehouseInventory
from apps.policies.models import RoutingPolicy
from apps.warehouses.models import Warehouse


class RouteOptimizer:

    def __init__(self):
        self.policy = (
            RoutingPolicy.objects
            .filter(is_active=True)
            .order_by("-updated_at")
            .first()
        )

        if not self.policy:
            raise ValueError("No active routing policy found.")

    @staticmethod
    def calculate_distance(
        warehouse_latitude,
        warehouse_longitude,
        customer_latitude,
        customer_longitude,
    ):
        earth_radius_km = 6371

        lat1 = radians(float(warehouse_latitude))
        lon1 = radians(float(warehouse_longitude))
        lat2 = radians(float(customer_latitude))
        lon2 = radians(float(customer_longitude))

        delta_latitude = lat2 - lat1
        delta_longitude = lon2 - lon1

        a = (
            sin(delta_latitude / 2) ** 2
            + cos(lat1)
            * cos(lat2)
            * sin(delta_longitude / 2) ** 2
        )

        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return earth_radius_km * c

    def optimize(
        self,
        sku_id,
        quantity,
        customer_latitude,
        customer_longitude,
    ):
        warehouses = (
            Warehouse.objects
            .filter(
                is_active=True,
                inventories__sku_id=sku_id,
                inventories__quantity__gte=quantity,
            )
            .distinct()
        )

        if not warehouses.exists():
            raise ValueError(
                "No warehouse has enough available inventory."
            )

        candidates = []

        for warehouse in warehouses:

            inventory = (
                WarehouseInventory.objects
                .filter(
                    warehouse=warehouse,
                    sku_id=sku_id,
                )
                .first()
            )

            if not inventory:
                continue

            available_quantity = (
                inventory.quantity
                - inventory.reserved_quantity
            )

            if available_quantity < quantity:
                continue

            distance_km = self.calculate_distance(
                warehouse.latitude,
                warehouse.longitude,
                customer_latitude,
                customer_longitude,
            )

            estimated_delivery_time = (
                distance_km / 40 * 60
            ) + (
                warehouse.processing_time_seconds / 60
            )

            traffic_factor = 1 + (
                self.policy.traffic_weight * 0.1
            )

            estimated_delivery_time *= traffic_factor

            transportation_cost = distance_km * 10

            total_cost = (
                transportation_cost
                + (
                    estimated_delivery_time
                    * self.policy.time_weight
                )
            )

            score = self.calculate_score(
                distance_km=distance_km,
                delivery_time=estimated_delivery_time,
                total_cost=total_cost,
                warehouse=warehouse,
            )

            candidates.append(
                {
                    "warehouse": warehouse,
                    "distance_km": round(
                        distance_km,
                        2,
                    ),
                    "estimated_delivery_time": round(
                        estimated_delivery_time,
                        2,
                    ),
                    "total_cost": round(
                        total_cost,
                        2,
                    ),
                    "score": round(
                        score,
                        2,
                    ),
                }
            )

        if not candidates:
            raise ValueError(
                "No suitable warehouse found."
            )

        best_candidate = max(
            candidates,
            key=lambda candidate: candidate["score"],
        )

        warehouse = best_candidate["warehouse"]

        return {
            "warehouse_id": warehouse.id,
            "warehouse_code": warehouse.code,
            "warehouse_name": warehouse.name,
            "estimated_delivery_time": (
                best_candidate[
                    "estimated_delivery_time"
                ]
            ),
            "total_cost": best_candidate[
                "total_cost"
            ],
            "route_optimization_score": (
                best_candidate["score"]
            ),
            "distance_km": best_candidate[
                "distance_km"
            ],
        }

    def calculate_score(
        self,
        distance_km,
        delivery_time,
        total_cost,
        warehouse,
    ):
        distance_score = 1 / (
            1 + distance_km
        )

        time_score = 1 / (
            1 + delivery_time
        )

        cost_score = 1 / (
            1 + total_cost
        )

        fleet_priority_score = (
            warehouse.heavy_fleet_priority
            / 100
        )

        score = (
            distance_score
            * self.policy.distance_weight
        )

        score += (
            time_score
            * self.policy.time_weight
        )

        score += (
            cost_score
            * self.policy.cost_weight
        )

        score += (
            fleet_priority_score
            * self.policy.traffic_weight
        )

        return score * 100