import { useState } from "react";
import "./App.css";

type Place = {
  name: string;
  address: string;
  rating: number | string;
  review_count?: number;
  distance_miles?: number | null;
  open_now?: boolean | null;
  weekday_descriptions?: string[];
  types: string[];
  photo_name?: string;
};

type Cards = {
  current_location: string;
  time_of_day: string;
  recommendation_focus: string[];
  food: {
    top_rated: Place | null;
    healthy: Place | null;
    different_cuisine: Place | null;
  };
  photo_spot: Place | null;
  experience: Place[];
  safety_tip: string;
};

function App() {
  const [cards, setCards] = useState<Cards | null>(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const startAutoMode = () => {
    setLoading(true);
    setCards(null);
    setMessage("");

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const response = await fetch("http://127.0.0.1:8000/auto-suggest-v2", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
            movement_status: "moving",
            stationary_minutes: 5,
            last_suggestion_minutes: 30,
          }),
        });

        const data = await response.json();

        if (data.suggest_now) {
          setCards(data.cards);
        } else {
          setMessage(`No suggestion right now. Reason: ${data.reason}`);
        }

        setLoading(false);
      },
      () => {
        setMessage("Location permission denied. Please allow location access.");
        setLoading(false);
      }
    );
  };
  const getTodayHours = (place: Place) => {
  if (!place.weekday_descriptions || place.weekday_descriptions.length === 0) {
    return null;
  }

  const today = new Date().toLocaleDateString("en-US", {
    weekday: "long",
  });

  return place.weekday_descriptions.find((day) =>
    day.toLowerCase().startsWith(today.toLowerCase())
  );
};
const formatReviews = (count?: number) => {
  if (!count) return "";
  if (count >= 1000) return `${(count / 1000).toFixed(1)}K`;
  return count.toString();
};

  const renderPlaceCard = (title: string, emoji: string, place: Place | null) => {
    if (!place) return null;

    return (
        <div className={`recommendation-card ${title.toLowerCase().replaceAll(" ", "-")}`}>  
        {place.photo_name && (
  <img
    className="place-image"
    src={`http://127.0.0.1:8000/photo?photo_name=${encodeURIComponent(
      place.photo_name
    )}`}
    alt={place.name}
  />
)}   
        <h3>{emoji} {title}</h3>
        <h4>{place.name}</h4>
        <p>{place.address}</p>
        <p>
  ⭐ {place.rating}
  {place.review_count ? ` • ${formatReviews(place.review_count)} reviews` : ""}
</p>

{place.open_now !== undefined && place.open_now !== null && (
  <p>{place.open_now ? "🟢 Open Now" : "🔴 Closed"}</p>
)}

{getTodayHours(place) && (
  <p>⏱ {getTodayHours(place)}</p>
)}

{place.distance_miles !== null && place.distance_miles !== undefined && (
  <p>📍 {place.distance_miles} mi</p>
)}
        <div className="card-footer">
  <a
    className="directions-button"
    href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(
      place.name + " " + place.address
    )}`}
    target="_blank"
    rel="noreferrer"
  >
    Get Directions →
  </a>
</div>
      </div>
    );
  };

  return (
    <div className="app">
      <div className="card">
        <h1>WanderCue</h1>
<p className="subtitle">Discover nearby places tailored for your day.</p>
        <button onClick={startAutoMode} disabled={loading}>
          {loading ? "Finding nearby places..." : "Discover Nearby"}
        </button>

        {message && <p className="message">{message}</p>}

        {cards && (
          <div className="dashboard">
            <div className="location-card">
              <h2>📍 Current Location</h2>
              <p>{cards.current_location}</p>
              <span>{cards.time_of_day}</span>
            </div>

            {renderPlaceCard("Recommended Restaurant", "⭐", cards.food.top_rated)}
            {renderPlaceCard("Healthy Choice", "🌿", cards.food.healthy)}
            {renderPlaceCard("Try Something Different", "🌎", cards.food.different_cuisine)}
            {renderPlaceCard("Perfect Photo Spot", "📸", cards.photo_spot)}
            {cards.experience &&
            cards.experience.map((place, index) =>
            renderPlaceCard(
            index === 0
            ? "Explore Nearby"
            : index === 1
            ? "Worth Visiting"
            : "Fun Activity",
             "🎯",
            place
          )
  )}

            <div className="recommendation-card safety">
              <h3>⚠ Safety Tip</h3>
              <p>{cards.safety_tip}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
