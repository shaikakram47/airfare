from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class FlightRecord(Base):
    __tablename__ = "flight_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    airline: Mapped[str] = mapped_column(String(64), nullable=False)
    source_city: Mapped[str] = mapped_column(String(64), nullable=False)
    destination_city: Mapped[str] = mapped_column(String(64), nullable=False)
    departure_time: Mapped[str] = mapped_column(String(32), nullable=False)
    arrival_time: Mapped[str] = mapped_column(String(32), nullable=False)
    stops: Mapped[str] = mapped_column(String(32), nullable=False)
    travel_class: Mapped[str] = mapped_column(String(32), nullable=False)
    duration: Mapped[float] = mapped_column(Float, nullable=False)
    days_left: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ModelMetric(Base):
    __tablename__ = "model_metrics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    model_name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    rmse: Mapped[float] = mapped_column(Float, nullable=False)
    mae: Mapped[float] = mapped_column(Float, nullable=False)
    r2: Mapped[float] = mapped_column(Float, nullable=False)
    is_best: Mapped[int] = mapped_column(Integer, default=0)
    trained_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
