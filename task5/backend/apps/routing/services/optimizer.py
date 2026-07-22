from .scoring import calculate_score


def select_best_warehouse(
    candidates,
    policy
):

    scored_candidates = []

    for candidate in candidates:

        score = calculate_score(

            candidate,

            candidates,

            policy

        )

        candidate["route_optimization_score"] = (

            score

        )

        scored_candidates.append(

            candidate

        )

    scored_candidates.sort(

        key=lambda item:

        item[

            "route_optimization_score"

        ],

        reverse=True

    )

    if not scored_candidates:

        return None

    return scored_candidates[0]