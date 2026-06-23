from datetime import datetime

def get_time_context():
    current_hour = datetime.now().hour

    if 5 <= current_hour < 11:
        return {
            "time_of_day": "morning",
            "recommendation_focus": ["coffee", "breakfast", "sunrise spots", "peaceful walks"]
        }

    if 11 <= current_hour < 17:
        return {
            "time_of_day": "afternoon",
            "recommendation_focus": ["food", "photo spots", "attractions", "experiences"]
        }

    if 17 <= current_hour < 20:
        return {
            "time_of_day": "evening",
            "recommendation_focus": ["sunset spots", "dinner", "golden-hour photo spots"]
        }

    return {
        "time_of_day": "night",
        "recommendation_focus": ["night views", "safe public places", "popular nightlife"]
    }
