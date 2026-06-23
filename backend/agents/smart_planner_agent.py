def create_trip_plan(destination, available_time, interests, suggestions):
    interests_text = ", ".join(interests).lower()

    plan = f"""
==================================
WanderCue Travel Plan
==================================

Trip: {destination}
Time Context: {available_time}
Interests: {', '.join(interests)}

"""

    if "food" in interests_text or "eat" in interests_text:
        plan += f"""
🍴 Food Recommendation:
{suggestions['food']}
"""

    if "photo" in interests_text or "spot" in interests_text or "view" in interests_text:
        plan += f"""
📸 Photo Spot:
{suggestions['photo_spot']}
"""

    if "experience" in interests_text or "vibe" in interests_text or "unique" in interests_text:
        plan += f"""
🎯 Local Experience / Vibe:
{suggestions['experience']}
"""

    plan += f"""
🗺 Suggested Plan:
Based on your current time and location, start with the most relevant nearby spot, then try food or a quick local experience if it fits.
⚠ Safety Tip:
{suggestions['safety']}
"""

    return plan
