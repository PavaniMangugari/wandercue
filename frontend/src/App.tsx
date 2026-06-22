import { useState } from "react";
import "./App.css";

function App() {
  const [destination, setDestination] = useState("");
  const [availableTime, setAvailableTime] = useState("");
  const [interests, setInterests] = useState("");
  const [plan, setPlan] = useState("");
  const [loading, setLoading] = useState(false);

  const generatePlan = async () => {
    try {
      setLoading(true);
      setPlan("");

      const response = await fetch("http://127.0.0.1:8000/plan", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          destination,
          available_time: availableTime,
          interests: interests.split(",").map((item) => item.trim()),
        }),
      });

      const data = await response.json();
      setPlan(data.plan);
    } catch (error) {
      setPlan("Error connecting to WanderCue backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="card">
        <h1>WanderCue</h1>
        <p className="subtitle">Your on-the-go AI travel companion</p>

        <input
          type="text"
          placeholder="Destination e.g. Las Vegas"
          value={destination}
          onChange={(e) => setDestination(e.target.value)}
        />

        <input
          type="text"
          placeholder="Available time e.g. 2 hours"
          value={availableTime}
          onChange={(e) => setAvailableTime(e.target.value)}
        />

        <input
          type="text"
          placeholder="Interests e.g. food, photos, experience"
          value={interests}
          onChange={(e) => setInterests(e.target.value)}
        />

        <button onClick={generatePlan} disabled={loading}>
          {loading ? "Creating Plan..." : "Generate WanderCue Plan"}
        </button>

        {plan && <pre className="result">{plan}</pre>}
      </div>
    </div>
  );
}

export default App;
