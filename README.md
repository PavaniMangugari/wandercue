# WanderCue

WanderCue is an AI-powered travel recommendation assistant that provides personalized recommendations based on a user's current location and time of day. It helps users discover restaurants, scenic photo spots, and nearby attractions while displaying ratings, business hours, and Google Maps directions.

---

## Features

- 📍 Detects the user's current location
- 🤖 Generates personalized recommendations using a multi-agent architecture
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
  
### APIs & Services
- Google Places API
- Google Geocoding API
- Google Gemini SDK (configured for future AI enhancements)
- Browser Geolocation API

---
## Architecture

```
                                  User
                  │
                  ▼
      React + TypeScript Frontend
                  │
          HTTP (REST API)
                  │
                  ▼
          FastAPI Backend (API)
                  │
                  ▼
         Coordinator Agent
                  │
      ┌───────────┴───────────┐
      ▼                       ▼
Local Discovery Agent    Smart Planner Agent
      │                       │
      └───────────┬───────────┘
                  ▼
     Recommendation Formatter
                  │
                  ▼
     Google Places & Geocoding APIs
                  │
                  ▼
      Formatted Recommendation Cards
                  │
                  ▼
      React User Interface
```
---

## AI Concepts Demonstrated
These concepts work together to provide personalized, context-aware travel recommendations using real-time location data and external services.

- Multi-agent architecture
- Context-aware recommendations
- Location-based personalization
- External API integration
- AI-ready architecture with Google Gemini SDK integration

---

## System Components

### Frontend
- React
- TypeScript
- Responsive recommendation cards
- Google Maps integration

### Backend
- FastAPI
- Recommendation formatter
- AI agent orchestration
- Business logic

### AI Agents
- Coordinator Agent
- Local Discovery Agent
- Smart Planner Agent

### External Services
- Google Places API
- Google Geocoding API
- Browser Geolocation API

---
## Recommendation Categories

Each recommendation may include:

- ⭐ Recommended Restaurant
- 🌿 Healthy Choice (when available)
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
│   ├── skills/
│   ├── api.py
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── .gitignore
└── README.md
```

---

## Prerequisites

Before running the project, make sure you have:

- Python 3.10+
- Node.js 18+
- npm
- Google Places API Key
- Google Geocoding API Key

---

## Environment Variables

Create a `.env` file inside the `backend` directory and add the required API keys.

```env
GOOGLE_PLACES_API_KEY=your_google_places_api_key
GEMINI_API_KEY=your_gemini_api_key
```

> **Note:** The Google Gemini SDK is configured for future AI-powered enhancements. The current implementation primarily uses the Google Places API due to Gemini API quota limitations.

---
## How to Run the Project

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn api:app --reload
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

- AI-generated travel itineraries
- Personalized recommendations based on user preferences
- Weather-aware suggestions
- Walking and cycling recommendations
- Save favorite places
- Recommendation history
---

## Author

**Pavani Mangugari**

AI Agents Capstone Project

GitHub: https://github.com/PavaniManggugari
