import os
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
GOOGLE_PLACES_URL = "https://places.googleapis.com/v1/places:searchNearby"
    
def search_nearby_places(
    latitude, longitude, included_types, radius=3000, max_results=5
):
    if not GOOGLE_PLACES_API_KEY:
        return []

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_PLACES_API_KEY,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.rating,places.userRatingCount,places.types,places.location,places.currentOpeningHours,places.photos",
    }

    payload = {
        "includedTypes": included_types,
        "maxResultCount": max_results,
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": latitude,
                    "longitude": longitude,
                },
                "radius": radius,
            }
        },
    }

    try:
        response = requests.post(
            GOOGLE_PLACES_URL,
            headers=headers,
            json=payload,
            timeout=10,
        )

        response.raise_for_status()
        data = response.json()

        places = []

        for place in data.get("places", []):
            location = place.get("location", {})

            places.append(
                {
                    "name": place.get("displayName", {}).get("text", "Unknown place"),
                    "address": place.get("formattedAddress", "Address not available"),
                    "rating": place.get("rating", "No rating"),
                    "review_count": place.get("userRatingCount", 0),
                    "types": place.get("types", []),
                    "latitude": location.get("latitude"),
                    "longitude": location.get("longitude"),
                    "open_now": place.get("currentOpeningHours", {}).get("openNow"),
                    "photo_name": place.get("photos", [{}])[0].get("name") if place.get("photos") else None,
                    "weekday_descriptions": place.get("currentOpeningHours", {}).get(
                    "weekdayDescriptions", []
                    ),
                }
            )

        return places

    except Exception as error:
        print("Google Places API failed.")
        print(error)
        return []


def get_food_types_by_time(time_of_day):
    if time_of_day == "morning":
        return ["cafe", "breakfast_restaurant", "bakery"]

    if time_of_day == "afternoon":
        return [
            "restaurant",
            "indian_restaurant",
            "italian_restaurant",
            "mexican_restaurant",
            "chinese_restaurant",
            "mediterranean_restaurant",
            "vegetarian_restaurant",
            "sandwich_shop",
        ]

    if time_of_day == "evening":
        return [
            "restaurant",
            "indian_restaurant",
            "italian_restaurant",
            "mexican_restaurant",
            "thai_restaurant",
            "japanese_restaurant",
            "mediterranean_restaurant",
        ]

    if time_of_day == "night":
        return ["restaurant", "bar", "night_club"]

    return ["restaurant"]


def get_attraction_types_by_time(time_of_day):
    common_types = [
        "tourist_attraction",
        "museum",
        "art_gallery",
        "botanical_garden",
        "amusement_park",
        "zoo",
        "aquarium",
        "historical_place",
        "hiking_area",
        "visitor_center"
    ]

    if time_of_day == "morning":
        return common_types + [
            "park",
            "botanical_garden",
            "hiking_area"
        ]

    if time_of_day == "afternoon":
        return common_types + [
            "museum",
            "park"
        ]

    if time_of_day == "evening":
        return common_types + [
            "tourist_attraction"
        ]

    if time_of_day == "night":
        return [
            "tourist_attraction",
            "bar",
            "night_club",
            "movie_theater",
            "bowling_alley"
        ]

    return common_types


def get_places_for_wandercue(latitude, longitude, time_of_day="afternoon"):
    food_types = get_food_types_by_time(time_of_day)
    attraction_types = get_attraction_types_by_time(time_of_day)

    food_places = search_nearby_places(
        latitude,
        longitude,
        food_types,
        radius=3000,
        max_results=10,
    )

    healthy_food_places = search_nearby_places(
        latitude,
        longitude,
        [
            "salad_shop",
            "vegan_restaurant",
            "health_food_restaurant",
            "juice_shop",
            "acai_shop",
            "mediterranean_restaurant",
        ],
        radius=5000,
        max_results=8,
    )

    attraction_places = search_nearby_places(
        latitude,
        longitude,
        attraction_types,
        radius=15000,
        max_results=15,
    )

    nightlife_places = []

    if time_of_day == "night":
        nightlife_places = search_nearby_places(
            latitude,
            longitude,
            ["bar", "night_club"],
            radius=15000,
            max_results=10,
        )

    return {
        "food_places": food_places,
        "healthy_food_places": healthy_food_places,
        "attraction_places": attraction_places,
        "nightlife_places": nightlife_places,
    }
