import { NavLink, Outlet } from "react-router-dom";
import "./Layout.css";

export default function Layout() {
  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand">
          <span className="brand-mark" aria-hidden="true">
            ✈
          </span>
          <div>
            <p className="brand-eyebrow">Airline Fare Prediction</p>
            <h1 className="brand-title">FareCast</h1>
          </div>
        </div>
        <nav className="nav">
          <NavLink to="/" end className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}>
            Predict
          </NavLink>
          <NavLink to="/models" className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}>
            Models
          </NavLink>
          <NavLink to="/about" className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}>
            About
          </NavLink>
        </nav>
      </header>
      <main className="main-content">
        <Outlet />
      </main>
      <footer className="footer">
        <p>Powered by FastAPI regression models · Vite + React</p>
      </footer>
    </div>
  );
}
