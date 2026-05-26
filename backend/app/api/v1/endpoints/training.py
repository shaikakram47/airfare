from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import ModelMetric
from app.schemas.prediction import ModelMetricOut, TrainResponse
from app.services.training_service import train_and_store_metrics

router = APIRouter()


@router.get("/metrics", response_model=list[ModelMetricOut])
def get_metrics(db: Session = Depends(get_db)):
    rows = db.query(ModelMetric).order_by(ModelMetric.rmse).all()
    if not rows:
        raise HTTPException(status_code=404, detail="No trained models found. POST /api/train first.")
    return [
        ModelMetricOut(
            model_name=row.model_name,
            rmse=row.rmse,
            mae=row.mae,
            r2=row.r2,
            is_best=bool(row.is_best),
        )
        for row in rows
    ]


@router.post("/train", response_model=TrainResponse)
def train_models(db: Session = Depends(get_db)):
    try:
        result = train_and_store_metrics(db)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Training failed: {exc}") from exc

    return TrainResponse(
        message="Models trained and stored successfully.",
        best_model=result["best_model"],
        training_samples=result["training_samples"],
        metrics=[
            ModelMetricOut(
                model_name=m["model_name"],
                rmse=m["rmse"],
                mae=m["mae"],
                r2=m["r2"],
                is_best=m["is_best"],
            )
            for m in result["metrics"]
        ],
    )
