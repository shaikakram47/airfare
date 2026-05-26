"""Sklearn preprocessing pipeline for fare regression."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from ml.constants import CATEGORICAL_COLUMNS, NUMERIC_COLUMNS


def build_preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                CATEGORICAL_COLUMNS,
            ),
            ("num", StandardScaler(), NUMERIC_COLUMNS),
        ]
    )


def build_training_pipeline(estimator) -> Pipeline:
    return Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            ("regressor", estimator),
        ]
    )


def flight_input_to_row(payload: dict) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "airline": payload["airline"],
                "source_city": payload["source_city"],
                "destination_city": payload["destination_city"],
                "departure_time": payload["departure_time"],
                "arrival_time": payload["arrival_time"],
                "stops": payload["stops"],
                "class": payload.get("class") or payload.get("class_type"),
                "duration": float(payload["duration"]),
                "days_left": int(payload["days_left"]),
            }
        ]
    )


def save_feature_metadata(path: Path) -> None:
    from ml.constants import AIRLINES, CITIES, CLASSES, STOPS, TIME_BUCKETS

    metadata = {
        "categorical_columns": CATEGORICAL_COLUMNS,
        "numeric_columns": NUMERIC_COLUMNS,
        "airlines": AIRLINES,
        "cities": CITIES,
        "time_buckets": TIME_BUCKETS,
        "stops": STOPS,
        "classes": CLASSES,
        "steps": [
            "Validate flight attributes from API payload",
            "One-hot encode categorical features (airline, cities, times, stops, class)",
            "Standard-scale numeric features (duration, days_left)",
            "Feed transformed matrix into regression model",
        ],
    }
    path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")


def load_feature_metadata(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
