"""Model comparison and best-model selection."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


@dataclass
class ModelScore:
    name: str
    rmse: float
    mae: float
    r2: float
    estimator: object

    def to_dict(self) -> dict:
        return {
            "model_name": self.name,
            "rmse": round(self.rmse, 4),
            "mae": round(self.mae, 4),
            "r2": round(self.r2, 4),
        }


def evaluate_model(name: str, pipeline, X_test, y_test) -> ModelScore:
    predictions = pipeline.predict(X_test)
    rmse = float(np.sqrt(mean_squared_error(y_test, predictions)))
    mae = float(mean_absolute_error(y_test, predictions))
    r2 = float(r2_score(y_test, predictions))
    return ModelScore(name=name, rmse=rmse, mae=mae, r2=r2, estimator=pipeline)


def split_features_target(df, feature_columns: list[str], target_column: str):
    X = df[feature_columns]
    y = df[target_column]
    return train_test_split(X, y, test_size=0.2, random_state=42)


def select_best_model(scores: list[ModelScore]) -> ModelScore:
    return min(scores, key=lambda item: item.rmse)
