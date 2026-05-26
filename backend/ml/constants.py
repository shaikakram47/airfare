"""Shared constants for the ML pipeline."""

CATEGORICAL_COLUMNS = [
    "airline",
    "source_city",
    "destination_city",
    "departure_time",
    "arrival_time",
    "stops",
    "class",
]
NUMERIC_COLUMNS = ["duration", "days_left"]
TARGET_COLUMN = "price"
FEATURE_COLUMNS = CATEGORICAL_COLUMNS + NUMERIC_COLUMNS

AIRLINES = ["SpiceJet", "AirAsia", "Vistara", "GO_FIRST", "Indigo", "Air_India"]
CITIES = ["Delhi", "Mumbai", "Bangalore", "Kolkata", "Hyderabad", "Chennai"]
TIME_BUCKETS = ["Morning", "Afternoon", "Evening", "Night"]
STOPS = ["zero", "one", "two_or_more"]
CLASSES = ["Economy", "Business"]

MODEL_DISPLAY_NAMES = {
    "linear_regression": "Linear Regression",
    "random_forest": "Random Forest Regression",
    "decision_tree": "Decision Tree Regression",
    "xgboost": "XGBoost Regression",
}
