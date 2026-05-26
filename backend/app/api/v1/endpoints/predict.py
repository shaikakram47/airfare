import math

from fastapi import APIRouter, HTTPException

from app.schemas.prediction import FlightInput, PredictionSummary
from ml.prediction.inference import get_best_model_name, predict_fare

router = APIRouter()


def _to_inference_payload(payload: FlightInput) -> dict:
    """Build a dict the ML pipeline expects (column name ``class``)."""
    return {
        "airline": payload.airline,
        "source_city": payload.source_city,
        "destination_city": payload.destination_city,
        "departure_time": payload.departure_time,
        "arrival_time": payload.arrival_time,
        "stops": payload.stops,
        "class": payload.class_type,
        "duration": payload.duration,
        "days_left": payload.days_left,
    }


@router.post("/predict", response_model=PredictionSummary)
def predict(payload: FlightInput):
    try:
        body = _to_inference_payload(payload)
        best_key = get_best_model_name()
        predicted_fare = predict_fare(body, best_key)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=503,
            detail="Models are not trained yet. Call POST /api/train to generate artifacts.",
        ) from exc

    if not math.isfinite(predicted_fare):
        raise HTTPException(
            status_code=500,
            detail="Model returned an invalid fare. Restart the API and run POST /api/train.",
        )

    return PredictionSummary(
        input=payload,
        predicted_fare=round(float(predicted_fare), 2),
    )
