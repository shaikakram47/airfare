from pydantic import BaseModel


class ProblemContext(BaseModel):
    title: str
    objective: str
    problem_type: str
    target_variable: str
    business_value: list[str]
    constraints: list[str]
    success_metrics: list[str]
    algorithms: list[str]


class FeatureEngineeringInfo(BaseModel):
    target: str | None = None
    feature_columns: list[str] | None = None
    categorical_columns: list[str]
    numeric_columns: list[str]
    steps: list[str]
    airlines: list[str] | None = None
    cities: list[str] | None = None
    time_buckets: list[str] | None = None
    stops: list[str] | None = None
    classes: list[str] | None = None
