import os
import json
from dotenv import load_dotenv
from google import genai

from data.sample_places import places
from services.google_places_service import get_places_for_wandercue

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def find_local_suggestions(destination, time_context=None, latitude=None, longitude=None):
    if latitude is not None and longitude is not None:
        google_places_result = get_google_places_suggestions(
            latitude,
            longitude,
            time_context
        )

        if google_places_result:
            return google_places_result

    ai_result = get_ai_suggestions(destination, time_context)

    if ai_result:
        return ai_result

    return get_fallback_suggestions(destination)


def get_google_places_suggestions(latitude, longitude, time_context=None):
    time_of_day = "afternoon"

    if time_context:
        time_of_day = time_context.get("time_of_day", "afternoon")

    places_data = get_places_for_wandercue(latitude, longitude, time_of_day)

    food_places = places_data.get("food_places", [])
    healthy_food_places = places_data.get("healthy_food_places", [])
    attraction_places = places_data.get("attraction_places", [])
    nightlife_places = places_data.get("nightlife_places", [])

    if not food_places and not attraction_places and not nightlife_places:
        return None

    return {
        "food": select_food_recommendations(food_places,healthy_food_places),
        "photo_spot": select_photo_spot(attraction_places),
        "experience": select_experience(attraction_places, nightlife_places),
        "safety": "Check opening hours, parking, weather, and local safety before visiting."
    }

def select_food_recommendations(food_places, healthy_food_places=None):
    if not food_places:
        return "No food suggestion found nearby."

    sorted_food = sorted(
        food_places,
        key=lambda place: place["rating"] if isinstance(place["rating"], (int, float)) else 0,
        reverse=True
    )

    top_food = sorted_food[0]

    healthy_food = None

    if healthy_food_places:
        sorted_healthy = sorted(
            healthy_food_places,
            key=lambda place: place["rating"] if isinstance(place["rating"], (int, float)) else 0,
            reverse=True
        )
        healthy_food = sorted_healthy[0]

    different_cuisine = next(
        (
            place for place in sorted_food
            if place["name"] != top_food["name"]
        ),
        None
    )

    food = f"""Top Rated Restaurant:
{top_food['name']}
{top_food['address']}
Rating: {top_food['rating']}"""

    if healthy_food:
        food += f"""

Healthy Food Option:
{healthy_food['name']}
{healthy_food['address']}
Rating: {healthy_food['rating']}"""

    if different_cuisine:
        food += f"""

Different Cuisine Option:
{different_cuisine['name']}
{different_cuisine['address']}
Rating: {different_cuisine['rating']}"""

    return food
   

def select_photo_spot(attraction_places):
    if not attraction_places:
        return "No photo spot found nearby."

    sorted_attractions = sorted(
        attraction_places,
        key=lambda place: place["rating"] if isinstance(place["rating"], (int, float)) else 0,
        reverse=True
    )

    photo_spot = sorted_attractions[0]

    return f"""{photo_spot['name']}
{photo_spot['address']}
Rating: {photo_spot['rating']}"""


def select_experience(attraction_places, nightlife_places):
    combined_places = attraction_places[1:] + nightlife_places

    if not combined_places:
        return "No local experience found nearby."

    sorted_places = sorted(
        combined_places,
        key=lambda place: place["rating"] if isinstance(place["rating"], (int, float)) else 0,
        reverse=True
    )

    experience = sorted_places[0]

    return f"""{experience['name']}
{experience['address']}
Rating: {experience['rating']}"""


def get_ai_suggestions(destination, time_context=None):
    try:
        time_of_day = "current time"
        recommendation_focus = ["food", "photo spots", "experiences"]

        if time_context:
            time_of_day = time_context.get("time_of_day", "current time")
            recommendation_focus = time_context.get(
                "recommendation_focus",
                ["food", "photo spots", "experiences"]
            )

        prompt = f"""
You are WanderCue, a proactive local travel discovery agent.

The user is currently near: {destination}
The current time context is: {time_of_day}
The recommendation focus is: {", ".join(recommendation_focus)}

Return JSON only in this exact format:
{{
  "food": "one local food, cafe, dessert, or restaurant suggestion",
  "photo_spot": "one scenic or photo-worthy spot suitable for this time",
  "experience": "one unique local experience or vibe suitable for this time",
  "safety": "one practical safety tip for this location and time"
}}

Rules:
- Keep each value under 30 words.
- Make recommendations local and realistic.
- Mention if opening hours should be verified.
- Avoid unsafe or isolated places at night.
"""

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        text = response.text.strip()

        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()
        elif text.startswith("```"):
            text = text.replace("```", "").strip()

        return json.loads(text)

    except Exception as error:
        print("Gemini failed. Using fallback data.")
        print(error)
        return None


def get_fallback_suggestions(destination):
    for city in places:
        if city.lower() == destination.lower():
            return places[city]

    return {
        "food": "Live local discovery is temporarily unavailable.",
        "photo_spot": "Try nearby scenic viewpoints, parks, or well-known public landmarks.",
        "experience": "Check nearby visitor centers, public attractions, or local event areas.",
        "safety": "Check weather, opening hours, parking, and local safety before visiting."
    }
