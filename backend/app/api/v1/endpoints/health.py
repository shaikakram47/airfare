from fastapi import APIRouter

from app.core.config import settings
from ml.constants import AIRLINES, CITIES, CLASSES, STOPS, TIME_BUCKETS
from ml.preprocessing.pipeline import load_feature_metadata

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok", "service": settings.app_name}


@router.get("/options")
def get_form_options():
    metadata_path = settings.artifacts_dir / "feature_metadata.json"
    if metadata_path.exists():
        return load_feature_metadata(metadata_path)
    return {
        "airlines": AIRLINES,
        "cities": CITIES,
        "time_buckets": TIME_BUCKETS,
        "stops": STOPS,
        "classes": CLASSES,
    }
