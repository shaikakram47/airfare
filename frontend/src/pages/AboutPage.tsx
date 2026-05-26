import "./AboutPage.css";

const models = [
  "Linear Regression",
  "Random Forest Regression",
  "Decision Tree Regression",
  "XGBoost Regression",
];

export default function AboutPage() {
  return (
    <div className="about-page">
      <section className="card about-intro">
        <h2>About FareCast</h2>
        <p>
          This system predicts domestic airline fares using four regression algorithms. The
          backend stores flight records and evaluation metrics in a SQL database, while
          preprocessing, training, and model selection live in dedicated Python modules.
        </p>
      </section>

      <section className="card">
        <h3>Architecture</h3>
        <ul className="about-list">
          <li>
            <strong>Backend:</strong> FastAPI · SQLAlchemy (SQLite) · scikit-learn · XGBoost
          </li>
          <li>
            <strong>Frontend:</strong> Vite · React · TypeScript · React Router · Vanilla CSS
          </li>
          <li>
            <strong>API:</strong> <code>POST /api/predict</code> returns the predicted fare
          </li>
        </ul>
      </section>

      <section className="card">
        <h3>Algorithms</h3>
        <div className="chip-row">
          {models.map((name) => (
            <span key={name} className="chip">
              {name}
            </span>
          ))}
        </div>
      </section>
    </div>
  );
}
