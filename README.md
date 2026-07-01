# WanderCue

WanderCue is an AI-powered travel recommendation assistant that helps users discover nearby places based on their current location and time of day. It provides personalized suggestions for restaurants, photo spots, and local attractions with useful details such as ratings, business hours, and Google Maps directions.

---

## Features

- 📍 Detects the user's current location
- 🤖 Generates smart recommendations using AI agents
- 🍽️ Recommends highly rated restaurants
- 🌿 Suggests healthy food options
- 📸 Finds scenic photo spots
- 🎯 Recommends nearby attractions and activities
- ⭐ Displays ratings and review counts
- 🕒 Shows business hours and open/closed status
- 📏 Calculates distance from the user's location
- 🗺️ Opens directions directly in Google Maps

---

## Technologies Used

### Frontend
- React
- TypeScript
- CSS

### Backend
- Python
- FastAPI

### APIs
- Google Places API
- Google Geocoding API
- Browser Geolocation API

---

## Project Workflow

```
User
   │
   ▼
React Frontend
   │
   ▼
FastAPI Backend
   │
   ▼
Google Places API
   │
   ▼
Recommendation Engine
   │
   ▼
Personalized Recommendation Cards
```

---

## Recommendation Categories

- ⭐ Recommended Restaurant
- 🌎 Try Something Different
- 📸 Perfect Photo Spot
- 🎯 Explore Nearby
- 🎯 Worth Visiting
- 🎯 Fun Activity

Each recommendation includes:
- Place name
- Address
- Rating and reviews
- Open/Closed status
- Business hours
- Distance
- Google Maps directions

---

## Project Structure

```
wandercue/
│
├── backend/
│   ├── agents/
│   ├── services/
│   ├── api.py
│   └── main.py
│
├── frontend/
│   ├── src/
│   └── public/
│
└── README.md
```

---

## How to Run the Project

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open the application in your browser:

```
http://localhost:5173
```

---

## Demo Steps

1. Open the application.
2. Allow location access.
3. Click **Discover Nearby**.
4. View personalized recommendations.
5. Click **Get Directions** to open Google Maps.

---

## Future Improvements

- Driving time estimation
- Weather-based recommendations
- User preferences and favorites
- AI-generated day itineraries
- Recommendation history

---

## Author

**Pavani Mangugari**

Capstone Project – WanderCue