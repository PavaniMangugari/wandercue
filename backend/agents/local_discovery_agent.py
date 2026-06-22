import os
import json
from dotenv import load_dotenv
from google import genai

from data.sample_places import places

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def find_local_suggestions(destination):
    ai_result = get_ai_suggestions(destination)

    if ai_result:
        return ai_result

    return get_fallback_suggestions(destination)


def get_ai_suggestions(destination):
    try:
        prompt = f"""
You are WanderCue, a local travel discovery agent.

The user is traveling to: {destination}

Return JSON only in this exact format:
{{
  "food": "one local food or restaurant suggestion",
  "photo_spot": "one beautiful photo spot",
  "experience": "one unique local experience",
  "safety": "one practical safety tip"
}}

Keep each value under 30 words.
Mention if opening hours should be verified.
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
