import { useState } from "react";
import "./App.css";

function App() {
  const [plan, setPlan] = useState("");
  const [loading, setLoading] = useState(false);

  const startAutoMode = () => {
    setLoading(true);
    setPlan("");

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const response = await fetch("http://127.0.0.1:8000/auto-suggest", {
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
          setPlan(data.suggestion);
        } else {
          setPlan(`No suggestion right now.\nReason: ${data.reason}`);
        }

        setLoading(false);
      },
      () => {
        setPlan("Location permission denied. Please allow location access.");
        setLoading(false);
      }
    );
  };

  return (
    <div className="app">
      <div className="card">
        <h1>WanderCue</h1>
        <p className="subtitle">Your on-the-go AI travel companion</p>

        <button onClick={startAutoMode} disabled={loading}>
          {loading ? "Finding nearby suggestions..." : "Start WanderCue"}
        </button>

        {plan && <pre className="result">{plan}</pre>}
      </div>
    </div>
  );
}

export default App;