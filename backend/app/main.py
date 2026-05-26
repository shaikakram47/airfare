from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.database import SessionLocal, init_db
from app.services.training_service import train_and_store_metrics


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    db = SessionLocal()
    try:
        train_and_store_metrics(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title=settings.app_name,
    description="Regression-based airline fare prediction API",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/")
def root():
    return {
        "message": "Airline Fare Prediction API",
        "docs": "/docs",
        "pipeline": {
            "problem": "/api/analytics/problem",
            "eda": "/api/analytics/eda",
            "features": "/api/analytics/features",
            "metrics": "/api/metrics",
            "predict": "POST /api/predict",
        },
    }
