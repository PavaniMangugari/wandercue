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
- Vite
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

- Multi-agent architecture
- Context-aware recommendations
- Location-based personalization
- External API integration
- AI-ready architecture with Google Gemini SDK integration

These concepts work together to provide personalized, context-aware travel recommendations using real-time location data and external services.


---

## System Components

### Frontend
- React
- TypeScript
- Vite
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

The application can recommend:

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
- Node.js 22.13.0 (recommended)
- npm
- Google Places API Key
- Google Geocoding API Key

---

## Node Version

This project was developed using **Node.js 22.13.0**.

If you use **nvm**, run:

```bash
nvm use
```

or install Node.js 22.13.0 before running the frontend.

---

## Google Cloud Setup

Before running the application, create a Google Cloud project.

1. Go to <https://console.cloud.google.com/>
2. Create a new project.
3. Enable the following APIs:
   - Google Places API
   - Google Geocoding API
4. Go to **APIs & Services → Credentials**.
5. Click **Create Credentials → API Key**.
6. Copy the generated API key.
7. Use the generated API key in the .env file shown below.
8. Create a `.env` file inside the `backend` directory and add:

```env
GOOGLE_PLACES_API_KEY=your_google_api_key
```
---


> **Note:** The project includes the Google Gemini SDK for future AI-powered enhancements. The current implementation uses the Google Places API for recommendation generation, so only a Google Places API key is required to run the application.

---
## How to Run the Project

### Backend

```bash
cd backend

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

uvicorn api:app --reload
```

The backend will be available at:

```
http://127.0.0.1:8000
```

### Frontend

```bash
cd frontend
npm ci
npm run dev
```

The frontend will be available at:

```
http://localhost:5173
```

---

## Verify the Application

Once both servers are running:

- Backend: http://127.0.0.1:8000
- Frontend: http://localhost:5173

Open the frontend in your browser, allow location access, and click **Discover Nearby**.

> **Tip:** If the application does not display recommendations, verify that your Google Places API key is valid, the required APIs are enabled, and browser location access has been granted.

---


## Demo Steps

1. Open the application.
2. Allow browser location access when prompted.
3. Click Discover Nearby.
4. View personalized recommendations.
5. Click Get Directions to open Google Maps.

---

## Troubleshooting

### SSL Certificate Error (macOS)

If you encounter SSL certificate errors while accessing Google APIs, run:

```bash
python3 -m pip install --upgrade certifi
```

Restart the backend after installing.

---

### API Key Errors

Make sure:

- Google Places API is enabled.
- Google Geocoding API is enabled.
- The API key is correctly added to `.env`.

---

### Location Not Working

Allow location access in your browser.

---

### Frontend Dependency Issues

Delete `node_modules` and reinstall:

```bash
rm -rf node_modules
npm ci
```

> **Note:** `npm ci` installs the exact dependency versions from `package-lock.json`, ensuring a consistent development environment.

---

## Future Improvements

- AI-generated travel itineraries
- Personalized recommendations based on user preferences
- Weather-aware suggestions
- Walking and cycling recommendations
- Save favorite places
- Recommendation history and recent searches
---

## Author

**Pavani Mangugari**

AI Agents Capstone Project

GitHub: https://github.com/PavaniMangugari/wandercue