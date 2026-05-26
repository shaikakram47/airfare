import { FormEvent, useEffect, useState } from "react";
import type { FlightInput, FormOptions } from "../types/api";
import "./FlightForm.css";

const defaultForm: FlightInput = {
  airline: "Vistara",
  source_city: "Delhi",
  destination_city: "Mumbai",
  departure_time: "Evening",
  arrival_time: "Night",
  stops: "zero",
  class: "Economy",
  duration: 2.25,
  days_left: 3,
};

interface FlightFormProps {
  options: FormOptions | null;
  loading: boolean;
  onSubmit: (payload: FlightInput) => void;
}

export default function FlightForm({ options, loading, onSubmit }: FlightFormProps) {
  const [form, setForm] = useState<FlightInput>(defaultForm);

  useEffect(() => {
    if (!options) return;
    setForm((prev) => ({
      ...prev,
      airline: options.airlines.includes(prev.airline) ? prev.airline : options.airlines[0],
      source_city: options.cities.includes(prev.source_city) ? prev.source_city : options.cities[0],
      destination_city: options.cities.includes(prev.destination_city)
        ? prev.destination_city
        : options.cities[1] ?? options.cities[0],
    }));
  }, [options]);

  const handleChange = (field: keyof FlightInput, value: string | number) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    if (form.source_city === form.destination_city) {
      alert("Source and destination must be different cities.");
      return;
    }
    onSubmit(form);
  };

  if (!options) {
    return <div className="card skeleton">Loading form options…</div>;
  }

  return (
    <form className="card flight-form" onSubmit={handleSubmit}>
      <div className="form-header">
        <h2>Flight details</h2>
        <p>Submit a JSON-compatible payload to the FastAPI prediction endpoint.</p>
      </div>

      <div className="form-grid">
        <label>
          Airline
          <select value={form.airline} onChange={(e) => handleChange("airline", e.target.value)}>
            {options.airlines.map((item) => (
              <option key={item} value={item}>
                {item.replaceAll("_", " ")}
              </option>
            ))}
          </select>
        </label>

        <label>
          Source city
          <select
            value={form.source_city}
            onChange={(e) => handleChange("source_city", e.target.value)}
          >
            {options.cities.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>
        </label>

        <label>
          Destination city
          <select
            value={form.destination_city}
            onChange={(e) => handleChange("destination_city", e.target.value)}
          >
            {options.cities.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>
        </label>

        <label>
          Departure time
          <select
            value={form.departure_time}
            onChange={(e) => handleChange("departure_time", e.target.value)}
          >
            {options.time_buckets.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>
        </label>

        <label>
          Arrival time
          <select
            value={form.arrival_time}
            onChange={(e) => handleChange("arrival_time", e.target.value)}
          >
            {options.time_buckets.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>
        </label>

        <label>
          Stops
          <select value={form.stops} onChange={(e) => handleChange("stops", e.target.value)}>
            {options.stops.map((item) => (
              <option key={item} value={item}>
                {item.replaceAll("_", " ")}
              </option>
            ))}
          </select>
        </label>

        <label>
          Class
          <select value={form.class} onChange={(e) => handleChange("class", e.target.value)}>
            {options.classes.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>
        </label>

        <label>
          Duration (hours)
          <input
            type="number"
            min={0.5}
            max={24}
            step={0.25}
            value={form.duration}
            onChange={(e) => handleChange("duration", Number(e.target.value))}
          />
        </label>

        <label>
          Days left to departure
          <input
            type="number"
            min={0}
            max={365}
            value={form.days_left}
            onChange={(e) => handleChange("days_left", Number(e.target.value))}
          />
        </label>
      </div>

      <button className="btn-primary" type="submit" disabled={loading}>
        {loading ? "Predicting…" : "Predict fare"}
      </button>
    </form>
  );
}
