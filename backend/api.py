from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents.coordinator_agent import run_wandercue
from agents.location_agent import detect_location_context
from agents.movement_agent import analyze_movement
from agents.recommendation_decision_agent import should_recommend
from agents.time_context_agent import get_time_context
from services.google_places_service import get_places_for_wandercue
from agents.recommendation_formatter import build_card_recommendations

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TripRequest(BaseModel):
    destination: str
    available_time: str
    interests: list[str]


class AutoSuggestRequest(BaseModel):
    latitude: float
    longitude: float
    movement_status: str
    stationary_minutes: int
    last_suggestion_minutes: int


@app.get("/")
def home():
    return {"message": "WanderCue API is running"}


@app.post("/plan")
def generate_plan(request: TripRequest):
    plan = run_wandercue(request.destination, request.available_time, request.interests)

    return {
        "destination": request.destination,
        "available_time": request.available_time,
        "interests": request.interests,
        "plan": plan,
    }


@app.post("/auto-suggest")
def auto_suggest(request: AutoSuggestRequest):
    location = detect_location_context(request.latitude, request.longitude)

    movement_context = analyze_movement(
        request.movement_status, request.stationary_minutes
    )

    time_context = get_time_context()

    decision = should_recommend(
        location, movement_context, request.last_suggestion_minutes
    )

    if not decision["suggest_now"]:
        return {
            "suggest_now": False,
            "location": location,
            "reason": decision["reason"],
            "time_context": time_context,
        }

    suggestion = run_wandercue(
        location,
        time_context["time_of_day"],
        time_context["recommendation_focus"],
        time_context,
        request.latitude,
        request.longitude,
    )

    return {
        "suggest_now": True,
        "location": location,
        "reason": decision["reason"],
        "time_context": time_context,
        "suggestion": suggestion,
    }


@app.post("/auto-suggest-v2")
def auto_suggest_v2(request: AutoSuggestRequest):
    location = detect_location_context(request.latitude, request.longitude)

    movement_context = analyze_movement(
        request.movement_status, request.stationary_minutes
    )

    time_context = get_time_context()

    decision = should_recommend(
        location, movement_context, request.last_suggestion_minutes
    )

    if not decision["suggest_now"]:
        return {
            "suggest_now": False,
            "location": location,
            "reason": decision["reason"],
            "time_context": time_context,
        }

    places_data = get_places_for_wandercue(
        request.latitude, request.longitude, time_context["time_of_day"]
    )

    cards = build_card_recommendations(
        location, time_context, places_data, request.latitude, request.longitude
    )

    return {
        "suggest_now": True,
        "location": location,
        "reason": decision["reason"],
        "time_context": time_context,
        "cards": cards,
    }
