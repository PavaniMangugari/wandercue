def analyze_movement(movement_status, stationary_minutes):
    """
    Decides if the user is exploring or staying still.
    """

    if stationary_minutes >= 60:
        return {
            "is_exploring": False,
            "reason": "User has been stationary for more than one hour."
        }

    if movement_status.lower() in ["moving", "walking", "driving"]:
        return {
            "is_exploring": True,
            "reason": "User is actively moving around the destination."
        }

    return {
        "is_exploring": False,
        "reason": "User is not currently exploring."
    }
