def create_trip_plan(destination, available_time, interests, suggestions):

    plan = f"""
==================================
WanderCue Travel Plan
==================================

Destination: {destination}
Available Time: {available_time}
Interests: {', '.join(interests)}

🍴 Food Recommendation:
{suggestions['food']}

📸 Photo Spot:
{suggestions['photo_spot']}

🎯 Unique Experience:
{suggestions['experience']}

🗺 Suggested Plan:
1. Visit the photo spot.
2. Enjoy the unique experience.
3. Try the local food recommendation.

⚠ Safety Tip:
{suggestions['safety']}
"""

    return plan
