"""Orchestrate database seeding and model training."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.models import FlightRecord, ModelMetric
from ml.preprocessing.dataset import generate_synthetic_dataset, records_to_dataframe
from ml.training.trainer import persist_models, train_all_models


def seed_database(db: Session, n_samples: int = 2500) -> int:
    existing = db.query(FlightRecord).count()
    if existing >= 500:
        return existing

    db.query(FlightRecord).delete()
    df = generate_synthetic_dataset(n_samples=n_samples)

    for row in df.to_dict(orient="records"):
        db.add(
            FlightRecord(
                airline=row["airline"],
                source_city=row["source_city"],
                destination_city=row["destination_city"],
                departure_time=row["departure_time"],
                arrival_time=row["arrival_time"],
                stops=row["stops"],
                travel_class=row["class"],
                duration=row["duration"],
                days_left=row["days_left"],
                price=row["price"],
            )
        )

    db.commit()
    return db.query(FlightRecord).count()


def load_training_frame(db: Session):
    records = db.query(FlightRecord).all()
    rows = [
        {
            "airline": r.airline,
            "source_city": r.source_city,
            "destination_city": r.destination_city,
            "departure_time": r.departure_time,
            "arrival_time": r.arrival_time,
            "stops": r.stops,
            "class": r.travel_class,
            "duration": r.duration,
            "days_left": r.days_left,
            "price": r.price,
        }
        for r in records
    ]
    return records_to_dataframe(rows)


def train_and_store_metrics(db: Session) -> dict:
    count = seed_database(db)
    df = load_training_frame(db)
    best, scores = train_all_models(df)
    persist_models(best, scores)

    db.query(ModelMetric).delete()
    for score in scores:
        db.add(
            ModelMetric(
                model_name=score.name,
                rmse=score.rmse,
                mae=score.mae,
                r2=score.r2,
                is_best=1 if score.name == best.name else 0,
            )
        )
    db.commit()

    return {
        "best_model": best.name,
        "training_samples": count,
        "metrics": [
            {
                "model_name": s.name,
                "rmse": round(s.rmse, 4),
                "mae": round(s.mae, 4),
                "r2": round(s.r2, 4),
                "is_best": s.name == best.name,
            }
            for s in scores
        ],
    }
