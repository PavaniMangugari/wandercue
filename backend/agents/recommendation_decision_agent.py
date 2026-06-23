def should_recommend(location, movement_context, last_suggestion_minutes):
    """
    Decides whether WanderCue should suggest something now.
    """

    if location == "Unknown Location":
        return {
            "suggest_now": False,
            "reason": "Location is not recognized yet."
        }

    if not movement_context["is_exploring"]:
        return {
            "suggest_now": False,
            "reason": movement_context["reason"]
        }

    if last_suggestion_minutes < 20:
        return {
            "suggest_now": False,
            "reason": "A suggestion was already shown recently."
        }

    return {
        "suggest_now": True,
        "reason": "User is exploring and no recent suggestion was shown."
    }
