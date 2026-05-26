"""CLI entry point to seed SQL data and train regression models."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.db.database import SessionLocal, init_db  # noqa: E402
from app.services.training_service import train_and_store_metrics  # noqa: E402


def main() -> None:
    init_db()
    db = SessionLocal()
    try:
        result = train_and_store_metrics(db)
        print(f"Trained on {result['training_samples']} records.")
        print(f"Best model: {result['best_model']}")
        for metric in result["metrics"]:
            flag = " (best)" if metric["is_best"] else ""
            print(
                f"- {metric['model_name']}{flag}: "
                f"RMSE={metric['rmse']}, MAE={metric['mae']}, R2={metric['r2']}"
            )
    finally:
        db.close()


if __name__ == "__main__":
    main()
