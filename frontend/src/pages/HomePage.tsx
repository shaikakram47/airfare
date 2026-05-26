import { useEffect, useState } from "react";
import { checkHealth, fetchOptions, predictFare } from "../api/client";
import FlightForm from "../components/FlightForm";
import PredictionResults from "../components/PredictionResults";
import type { FlightInput, FormOptions, PredictionSummary } from "../types/api";
import "./HomePage.css";

export default function HomePage() {
  const [options, setOptions] = useState<FormOptions | null>(null);
  const [summary, setSummary] = useState<PredictionSummary | null>(null);
  const [loading, setLoading] = useState(false);
  const [apiOnline, setApiOnline] = useState<boolean | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchOptions()
      .then(setOptions)
      .catch(() => setError("Could not load form options from the API."));
    checkHealth()
      .then(() => setApiOnline(true))
      .catch(() => setApiOnline(false));
  }, []);

  const handlePredict = async (payload: FlightInput) => {
    setLoading(true);
    setError(null);
    try {
      const result = await predictFare(payload);
      setSummary(result);
    } catch (err) {
      setSummary(null);
      setError(err instanceof Error ? err.message : "Prediction failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="home-page">
      <section className="hero card">
        <div>
          <p className="hero-eyebrow">Fare prediction</p>
          <h2>Predict airline fares in seconds</h2>
          <p>Enter flight details to get a fare estimate from the best trained model.</p>
        </div>
        <div className={`status-pill ${apiOnline ? "online" : apiOnline === false ? "offline" : ""}`}>
          API {apiOnline === null ? "checking…" : apiOnline ? "online" : "offline"}
        </div>
      </section>

      {error && <div className="alert">{error}</div>}

      <div className="home-grid">
        <FlightForm options={options} loading={loading} onSubmit={handlePredict} />
        <PredictionResults summary={summary} />
      </div>
    </div>
  );
}
