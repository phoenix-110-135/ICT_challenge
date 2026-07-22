def normalize_value(
    value,
    minimum,
    maximum
):

    if maximum == minimum:

        return 1

    return (

        1

        -

        (

            value

            -

            minimum

        )

        /

        (

            maximum

            -

            minimum

        )

    )


def calculate_score(
    candidate,
    candidates,
    policy
):

    costs = [

        item["transportation_cost"]

        for item in candidates

    ]

    times = [

        item["estimated_time"]

        for item in candidates

    ]

    distances = [

        item["distance"]

        for item in candidates

    ]

    traffic_values = [

        item["traffic"]

        for item in candidates

    ]

    cost_score = normalize_value(

        candidate["transportation_cost"],

        min(costs),

        max(costs)

    )

    time_score = normalize_value(

        candidate["estimated_time"],

        min(times),

        max(times)

    )

    distance_score = normalize_value(

        candidate["distance"],

        min(distances),

        max(distances)

    )

    traffic_score = normalize_value(

        candidate["traffic"],

        min(traffic_values),

        max(traffic_values)

    )

    score = (

        cost_score

        *

        policy.cost_weight

    ) + (

        time_score

        *

        policy.time_weight

    ) + (

        distance_score

        *

        policy.distance_weight

    ) + (

        traffic_score

        *

        policy.traffic_weight

    )

    return round(

        score * 100,
        2
    )