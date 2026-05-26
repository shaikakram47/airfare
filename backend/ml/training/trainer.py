"""Train and persist regression models."""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from app.core.config import settings
from ml.constants import FEATURE_COLUMNS, TARGET_COLUMN
from ml.evaluation.selection import ModelScore, evaluate_model, select_best_model, split_features_target
from ml.preprocessing.pipeline import build_training_pipeline, save_feature_metadata


def get_model_estimators() -> dict[str, object]:
    return {
        "linear_regression": LinearRegression(),
        "random_forest": RandomForestRegressor(
            n_estimators=120, max_depth=14, random_state=42, n_jobs=-1
        ),
        "decision_tree": DecisionTreeRegressor(max_depth=12, random_state=42),
        "xgboost": XGBRegressor(
            n_estimators=150,
            max_depth=6,
            learning_rate=0.08,
            subsample=0.9,
            colsample_bytree=0.9,
            random_state=42,
            objective="reg:squarederror",
        ),
    }


def train_all_models(df: pd.DataFrame) -> tuple[ModelScore, list[ModelScore]]:
    X_train, X_test, y_train, y_test = split_features_target(df, FEATURE_COLUMNS, TARGET_COLUMN)
    scores: list[ModelScore] = []

    for name, estimator in get_model_estimators().items():
        pipeline = build_training_pipeline(estimator)
        pipeline.fit(X_train, y_train)
        scores.append(evaluate_model(name, pipeline, X_test, y_test))

    return select_best_model(scores), scores


def persist_models(best: ModelScore, scores: list[ModelScore]) -> Path:
    models_dir = settings.models_dir
    models_dir.mkdir(parents=True, exist_ok=True)

    for score in scores:
        joblib.dump(score.estimator, models_dir / f"{score.name}.joblib")

    joblib.dump(best.estimator, models_dir / "best_model.joblib")
    save_feature_metadata(settings.artifacts_dir / "feature_metadata.json")

    selection_path = settings.artifacts_dir / "model_selection.json"
    selection_path.write_text(
        pd.DataFrame([s.to_dict() for s in scores]).to_json(orient="records"),
        encoding="utf-8",
    )
    (settings.artifacts_dir / "best_model.txt").write_text(best.name, encoding="utf-8")
    return models_dir
