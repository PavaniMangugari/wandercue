from fastapi import FastAPI
from pydantic import BaseModel
from agents.coordinator_agent import run_wandercue

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
def home():
    return {"message": "WanderCue API is running"}

@app.post("/plan")
def generate_plan(request: TripRequest):
    plan = run_wandercue(
        request.destination,
        request.available_time,
        request.interests
    )

    return {
        "destination": request.destination,
        "available_time": request.available_time,
        "interests": request.interests,
        "plan": plan
    }
