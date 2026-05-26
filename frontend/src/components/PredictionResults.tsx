import type { PredictionSummary } from "../types/api";
import "./PredictionResults.css";

interface PredictionResultsProps {
  summary: PredictionSummary | null;
}

/** Support current API and older responses that used `recommended_fare`. */
function resolveFare(summary: PredictionSummary): number | null {
  const raw = summary.predicted_fare;
  if (typeof raw === "number" && Number.isFinite(raw)) {
    return raw;
  }

  const legacy = (summary as PredictionSummary & { recommended_fare?: number }).recommended_fare;
  if (typeof legacy === "number" && Number.isFinite(legacy)) {
    return legacy;
  }

  return null;
}

function formatCurrency(value: number, currency: string) {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency,
    maximumFractionDigits: 0,
  }).format(value);
}

export default function PredictionResults({ summary }: PredictionResultsProps) {
  if (!summary) {
    return (
      <div className="card results-empty">
        <h3>Predicted fare</h3>
        <p>Submit flight details to get a fare prediction.</p>
      </div>
    );
  }

  const fare = resolveFare(summary);

  if (fare === null) {
    return (
      <div className="card results-empty">
        <h3>Predicted fare</h3>
        <p className="results-error">
          Could not read a valid fare from the API. Restart the backend server so it runs the
          latest code, then try again.
        </p>
      </div>
    );
  }

  return (
    <div className="card results-panel">
      <p className="eyebrow">Predicted fare</p>
      <h2 className="fare-value">{formatCurrency(fare, summary.currency)}</h2>
      <p className="route-line">
        {summary.input.source_city} → {summary.input.destination_city}
      </p>
    </div>
  );
}
