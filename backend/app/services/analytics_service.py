"""Analytics and EDA service layer."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.config import settings
from app.services.training_service import load_training_frame, seed_database
from ml.eda.analyzer import build_eda_report
from ml.preprocessing.pipeline import load_feature_metadata


def get_eda_report(db: Session) -> dict:
    seed_database(db)
    df = load_training_frame(db)
    return build_eda_report(df)


def get_feature_engineering_info() -> dict:
    metadata_path = settings.artifacts_dir / "feature_metadata.json"
    if metadata_path.exists():
        return load_feature_metadata(metadata_path)

    from ml.constants import (
        AIRLINES,
        CATEGORICAL_COLUMNS,
        CITIES,
        CLASSES,
        FEATURE_COLUMNS,
        NUMERIC_COLUMNS,
        STOPS,
        TARGET_COLUMN,
        TIME_BUCKETS,
    )

    return {
        "target": TARGET_COLUMN,
        "feature_columns": FEATURE_COLUMNS,
        "categorical_columns": CATEGORICAL_COLUMNS,
        "numeric_columns": NUMERIC_COLUMNS,
        "airlines": AIRLINES,
        "cities": CITIES,
        "time_buckets": TIME_BUCKETS,
        "stops": STOPS,
        "classes": CLASSES,
        "steps": [
            "Validate flight attributes from API payload",
            "One-hot encode categorical features",
            "Standard-scale numeric features (duration, days_left)",
            "Feed transformed matrix into regression model",
        ],
    }


def get_problem_context() -> dict:
    return {
        "title": "Airline Fare Prediction",
        "objective": "Predict domestic flight ticket prices (INR) from route, schedule, and booking attributes.",
        "problem_type": "Supervised Regression",
        "target_variable": "price",
        "business_value": [
            "Help travelers estimate fair ticket prices before booking",
            "Support revenue teams with data-driven fare benchmarks",
            "Compare multiple regression algorithms for best accuracy",
        ],
        "constraints": [
            "Historical labeled data with price as target",
            "Categorical attributes require encoding before modeling",
            "Model must generalize to unseen routes and airlines",
        ],
        "success_metrics": ["RMSE", "MAE", "R²"],
        "algorithms": [
            "Linear Regression",
            "Random Forest Regression",
            "Decision Tree Regression",
            "XGBoost Regression",
        ],
    }
