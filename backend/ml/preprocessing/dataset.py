"""Dataset generation and frame utilities."""

from __future__ import annotations

import numpy as np
import pandas as pd

from ml.constants import AIRLINES, CITIES, CLASSES, STOPS, TIME_BUCKETS


def records_to_dataframe(records: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(records)
    if "class_type" in df.columns:
        df = df.rename(columns={"class_type": "class"})
    if "travel_class" in df.columns:
        df = df.rename(columns={"travel_class": "class"})
    return df


def generate_synthetic_dataset(n_samples: int = 2500, random_state: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(random_state)
    rows: list[dict] = []
    base_fares = {"Economy": 3500, "Business": 12000}

    for _ in range(n_samples):
        airline = rng.choice(AIRLINES)
        source = rng.choice(CITIES)
        destination = rng.choice([c for c in CITIES if c != source])
        travel_class = rng.choice(CLASSES, p=[0.85, 0.15])
        duration = float(rng.uniform(1.0, 12.0))
        days_left = int(rng.integers(1, 50))
        stops = rng.choice(STOPS, p=[0.55, 0.35, 0.10])

        price = base_fares[travel_class]
        price += duration * 420
        price += days_left * -35
        price += {"zero": 0, "one": 900, "two_or_more": 1800}[stops]
        price += {
            "SpiceJet": -400,
            "AirAsia": -300,
            "Vistara": 500,
            "GO_FIRST": -200,
            "Indigo": 0,
            "Air_India": 350,
        }[airline]
        price += rng.normal(0, 450)
        price = max(1500.0, price)

        rows.append(
            {
                "airline": airline,
                "source_city": source,
                "destination_city": destination,
                "departure_time": rng.choice(TIME_BUCKETS),
                "arrival_time": rng.choice(TIME_BUCKETS),
                "stops": stops,
                "class": travel_class,
                "duration": round(duration, 2),
                "days_left": days_left,
                "price": round(float(price), 2),
            }
        )

    return pd.DataFrame(rows)
