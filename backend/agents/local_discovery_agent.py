import os
import json
from dotenv import load_dotenv
from google import genai

from data.sample_places import places
from skills.food_skill import get_food_suggestion
from skills.photo_skill import get_photo_spot
from skills.experience_skill import get_experience_suggestion

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def find_local_suggestions(destination, time_context=None):
    ai_result = get_ai_suggestions(destination, time_context)

    if ai_result:
        return build_skill_response(ai_result)

    fallback_result = get_fallback_suggestions(destination)
    return build_skill_response(fallback_result)


def build_skill_response(place_data):
    return {
        "food": get_food_suggestion(place_data),
        "photo_spot": get_photo_spot(place_data),
        "experience": get_experience_suggestion(place_data),
        "safety": place_data.get(
            "safety",
            "Check weather, opening hours, parking, and local safety before visiting."
        )
    }


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

Suggest local recommendations that make sense for the current time of day.

Examples:
- Morning: coffee, breakfast, sunrise spots, peaceful walks
- Afternoon: food, attractions, photo spots, experiences
- Evening: sunset spots, dinner, golden-hour photos
- Night: safe public places, night views, popular nightlife

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
        "food": "No food suggestion found. Try checking a trusted maps or travel app.",
        "photo_spot": "No photo spot found. Try searching nearby scenic viewpoints.",
        "experience": "No experience found. Try checking local events or visitor centers.",
        "safety": "Check weather, opening hours, parking, and local safety before visiting."
    }
