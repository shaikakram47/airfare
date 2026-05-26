import { useEffect, useState } from "react";
import { fetchMetrics, trainModels } from "../api/client";
import type { ModelMetric } from "../types/api";
import "./ModelsPage.css";

const DISPLAY_NAMES: Record<string, string> = {
  linear_regression: "Linear Regression",
  random_forest: "Random Forest Regression",
  decision_tree: "Decision Tree Regression",
  xgboost: "XGBoost Regression",
};

export default function ModelsPage() {
  const [metrics, setMetrics] = useState<ModelMetric[]>([]);
  const [loading, setLoading] = useState(true);
  const [training, setTraining] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const loadMetrics = () => {
    setLoading(true);
    fetchMetrics()
      .then((data) => {
        setMetrics(data);
        setError(null);
      })
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load metrics."))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadMetrics();
  }, []);

  const handleRetrain = async () => {
    setTraining(true);
    setMessage(null);
    setError(null);
    try {
      const result = await trainModels();
      setMessage(result.message);
      setMetrics(result.metrics);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Training failed.");
    } finally {
      setTraining(false);
    }
  };

  return (
    <div className="models-page">
      <header className="models-header card">
        <div>
          <h2>Model performance</h2>
          <p>Metrics are stored in SQL after each training run. Lower RMSE is better.</p>
        </div>
        <button className="btn-primary" onClick={handleRetrain} disabled={training}>
          {training ? "Training…" : "Retrain models"}
        </button>
      </header>

      {message && <div className="alert success">{message}</div>}
      {error && <div className="alert">{error}</div>}

      <div className="metrics-grid">
        {loading && <div className="card skeleton">Loading metrics…</div>}
        {!loading &&
          metrics.map((metric) => (
            <article
              key={metric.model_name}
              className={`card metric-card ${metric.is_best ? "best" : ""}`}
            >
              <div className="metric-title-row">
                <h3>{DISPLAY_NAMES[metric.model_name] ?? metric.model_name}</h3>
                {metric.is_best && <span className="badge">Best</span>}
              </div>
              <dl className="metric-stats">
                <div>
                  <dt>RMSE</dt>
                  <dd>{metric.rmse.toFixed(2)}</dd>
                </div>
                <div>
                  <dt>MAE</dt>
                  <dd>{metric.mae.toFixed(2)}</dd>
                </div>
                <div>
                  <dt>R²</dt>
                  <dd>{metric.r2.toFixed(4)}</dd>
                </div>
              </dl>
            </article>
          ))}
      </div>
    </div>
  );
}
