from pydantic import BaseModel, Field


class FlightInput(BaseModel):
    airline: str = Field(..., examples=["Vistara"])
    source_city: str = Field(..., examples=["Delhi"])
    destination_city: str = Field(..., examples=["Mumbai"])
    departure_time: str = Field(..., examples=["Evening"])
    arrival_time: str = Field(..., examples=["Night"])
    stops: str = Field(..., examples=["zero"])
    class_type: str = Field(..., alias="class", examples=["Economy"])
    duration: float = Field(..., gt=0, examples=[2.25])
    days_left: int = Field(..., ge=0, le=365, examples=[1])

    model_config = {"populate_by_name": True}


class PredictionSummary(BaseModel):
    input: FlightInput
    predicted_fare: float
    currency: str = "INR"


class ModelMetricOut(BaseModel):
    model_name: str
    rmse: float
    mae: float
    r2: float
    is_best: bool


class TrainResponse(BaseModel):
    message: str
    best_model: str
    metrics: list[ModelMetricOut]
    training_samples: int
