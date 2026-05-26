"""Load models and run fare inference."""

from __future__ import annotations

import math
from pathlib import Path

import joblib
import numpy as np

from app.core.config import settings
from ml.preprocessing.pipeline import flight_input_to_row


def _models_dir() -> Path:
    return settings.models_dir


def load_model(model_name: str):
    path = _models_dir() / f"{model_name}.joblib"
    if not path.exists():
        raise FileNotFoundError(f"Model artifact not found: {model_name}")
    return joblib.load(path)


def get_best_model_name() -> str:
    marker = settings.artifacts_dir / "best_model.txt"
    if marker.exists():
        return marker.read_text(encoding="utf-8").strip()
    return "random_forest"


def predict_fare(payload: dict, model_name: str | None = None) -> float:
    if payload.get("class") is None and payload.get("class_type") is None:
        raise ValueError("Missing travel class ('class' field).")

    model_key = model_name or get_best_model_name()
    pipeline = load_model(model_key)
    raw = pipeline.predict(flight_input_to_row(payload))[0]
    value = float(raw)

    if not math.isfinite(value):
        raise ValueError(f"Model '{model_key}' returned a non-finite prediction.")

    return max(value, 500.0)
