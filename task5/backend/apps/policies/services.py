from .models import RoutingPolicy

def get_active_policy():

    policy = (
        RoutingPolicy.objects
        .filter(
            is_active=True
        )
        .order_by(
            "-created_at"
        )
        .first()
    )
    if policy:
        return policy
    
    return RoutingPolicy(
        
        name="Default Policy",
        cost_weight=0.4,
        time_weight=0.3,
        distance_weight=0.2,
        traffic_weight=0.1,
        is_active=True
    )