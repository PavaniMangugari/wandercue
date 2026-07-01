from math import radians, sin, cos, sqrt, atan2


def calculate_distance_miles(user_lat, user_lng, place_lat, place_lng):
    if (
        user_lat is None
        or user_lng is None
        or place_lat is None
        or place_lng is None
    ):
        return None

    earth_radius_miles = 3958.8

    lat1 = radians(user_lat)
    lon1 = radians(user_lng)
    lat2 = radians(place_lat)
    lon2 = radians(place_lng)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return round(earth_radius_miles * c, 1)


def format_place(place, user_lat=None, user_lng=None):
    if not place:
        return None

    distance = calculate_distance_miles(
        user_lat,
        user_lng,
        place.get("latitude"),
        place.get("longitude"),
    )

    return {
        "name": place.get("name", "Unknown place"),
        "address": place.get("address", "Address not available"),
        "rating": place.get("rating", "No rating"),
        "review_count": place.get("review_count", 0),
        "types": place.get("types", []),
        "distance_miles": distance,
        "open_now": place.get("open_now"),
        "weekday_descriptions": place.get("weekday_descriptions", []),
        "photo_name": place.get("photo_name"),
    }


def sort_by_rating(places):
    return sorted(
        places,
        key=lambda place: (
            place["rating"] if isinstance(place["rating"], (int, float)) else 0
        ),
        reverse=True,
    )


def select_healthy_food(healthy_places):
    healthy_priority = [
        "salad_shop",
        "vegan_restaurant",
        "health_food_restaurant",
        "juice_shop",
        "acai_shop",
        "mediterranean_restaurant",
    ]

    excluded_types = [
        "indian_restaurant",
        "chinese_restaurant",
        "italian_restaurant",
        "mexican_restaurant",
        "pizza_restaurant",
        "hamburger_restaurant",
        "fast_food_restaurant",
        "bar",
        "brewery",
        "pub",
    ]

    for place in healthy_places:
        place_types = place.get("types", [])

        has_healthy_type = any(t in place_types for t in healthy_priority)
        has_excluded_type = any(t in place_types for t in excluded_types)

        if has_healthy_type and not has_excluded_type:
            return place

    return None


def is_restaurant_or_food_place(place):
    restaurant_types = [
        "restaurant",
        "fast_food_restaurant",
        "cafe",
        "meal_takeaway",
        "meal_delivery",
        "pizza_restaurant",
        "hamburger_restaurant",
        "steak_house",
        "seafood_restaurant",
        "mexican_restaurant",
        "italian_restaurant",
        "chinese_restaurant",
        "indian_restaurant",
        "japanese_restaurant",
        "mediterranean_restaurant",
        "bar",
        "brewery",
        "pub",
    ]

    place_types = place.get("types", [])
    return any(t in place_types for t in restaurant_types)


def select_photo_spot(sorted_attractions):
    photo_types = [
        "park",
        "tourist_attraction",
        "botanical_garden",
        "nature_preserve",
        "national_park",
        "state_park",
        "garden",
        "museum",
        "historical_landmark",
        "monument",
        "observation_deck",
    ]

    bad_photo_types = [
        "restaurant",
        "fast_food_restaurant",
        "cafe",
        "bar",
        "brewery",
        "pub",
        "meal_takeaway",
    ]

    for place in sorted_attractions:
        place_types = place.get("types", [])

        is_good_photo_spot = any(t in place_types for t in photo_types)
        is_bad_photo_spot = any(t in place_types for t in bad_photo_types)

        if is_good_photo_spot and not is_bad_photo_spot:
            return place

    return sorted_attractions[0] if sorted_attractions else None


def select_experience_options(
    sorted_attractions,
    sorted_nightlife,
    photo_spot,
    user_lat=None,
    user_lng=None,
):
    experience_options = []

    for place in sorted_attractions:
        if photo_spot and place.get("name") == photo_spot.get("name"):
            continue

        if is_restaurant_or_food_place(place):
            continue

        formatted_place = format_place(place, user_lat, user_lng)

        if formatted_place:
            experience_options.append(formatted_place)

        if len(experience_options) == 3:
            break

    if not experience_options:
        for place in sorted_nightlife:
            if is_restaurant_or_food_place(place):
                continue

            formatted_place = format_place(place, user_lat, user_lng)

            if formatted_place:
                experience_options.append(formatted_place)

            if len(experience_options) == 3:
                break

    return experience_options
def get_cuisine_types(place):
    cuisine_types = [
        "mexican_restaurant",
        "italian_restaurant",
        "indian_restaurant",
        "chinese_restaurant",
        "thai_restaurant",
        "japanese_restaurant",
        "mediterranean_restaurant",
        "vietnamese_restaurant",
        "korean_restaurant",
        "greek_restaurant",
        "middle_eastern_restaurant",
    ]

    place_types = place.get("types", [])
    return [t for t in place_types if t in cuisine_types]


def select_different_cuisine(sorted_food, top_food):
    if not sorted_food or not top_food:
        return None

    top_cuisines = get_cuisine_types(top_food)

    excluded_types = [
        "bar",
        "brewery",
        "pub",
        "night_club",
        "fast_food_restaurant",
    ]

    for place in sorted_food:
        if place.get("name") == top_food.get("name"):
            continue

        place_types = place.get("types", [])

        if any(t in place_types for t in excluded_types):
            continue

        place_cuisines = get_cuisine_types(place)

        if place_cuisines and place_cuisines != top_cuisines:
            return place

    for place in sorted_food:
        if place.get("name") != top_food.get("name"):
            place_types = place.get("types", [])

            if not any(t in place_types for t in excluded_types):
                return place

    return None


def build_card_recommendations(
    location,
    time_context,
    places_data,
    user_lat=None,
    user_lng=None,
):
    food_places = places_data.get("food_places", [])
    healthy_food_places = places_data.get("healthy_food_places", [])
    attraction_places = places_data.get("attraction_places", [])
    nightlife_places = places_data.get("nightlife_places", [])

    sorted_food = sort_by_rating(food_places)
    sorted_healthy = sort_by_rating(healthy_food_places)
    sorted_attractions = sort_by_rating(attraction_places)
    sorted_nightlife = sort_by_rating(nightlife_places)

    top_food = sorted_food[0] if sorted_food else None
    healthy_food = select_healthy_food(sorted_healthy)

    different_cuisine = select_different_cuisine(sorted_food, top_food)

    photo_spot = select_photo_spot(sorted_attractions)

    experience_options = select_experience_options(
        sorted_attractions,
        sorted_nightlife,
        photo_spot,
        user_lat,
        user_lng,
    )

    return {
        "current_location": location,
        "time_of_day": time_context.get("time_of_day", "current time"),
        "recommendation_focus": time_context.get("recommendation_focus", []),
        "food": {
            "top_rated": format_place(top_food, user_lat, user_lng),
            "healthy": format_place(healthy_food, user_lat, user_lng),
            "different_cuisine": format_place(different_cuisine, user_lat, user_lng),
        },
        "photo_spot": format_place(photo_spot, user_lat, user_lng),
        "experience": experience_options,
        "safety_tip": "Check opening hours, parking, weather, and local safety before visiting.",
    }