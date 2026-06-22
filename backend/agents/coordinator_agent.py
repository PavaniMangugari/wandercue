from agents.local_discovery_agent import find_local_suggestions
from agents.smart_planner_agent import create_trip_plan

def run_wandercue(destination, available_time, interests):

    suggestions = find_local_suggestions(destination)

    final_plan = create_trip_plan(
        destination,
        available_time,
        interests,
        suggestions
    )

    return final_plan
