from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.analytics import FeatureEngineeringInfo, ProblemContext
from app.services.analytics_service import (
    get_eda_report,
    get_feature_engineering_info,
    get_problem_context,
)

router = APIRouter()


@router.get("/problem", response_model=ProblemContext)
def problem_understanding():
    return get_problem_context()


@router.get("/eda")
def exploratory_analysis(db: Session = Depends(get_db)):
    return get_eda_report(db)


@router.get("/features", response_model=FeatureEngineeringInfo)
def feature_engineering():
    return get_feature_engineering_info()
