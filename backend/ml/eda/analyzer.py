"""Exploratory data analysis summaries for the API."""

from __future__ import annotations

import pandas as pd


def dataset_overview(df: pd.DataFrame) -> dict:
    numeric = df.select_dtypes(include="number")
    return {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "features": [c for c in df.columns if c != "price"],
        "target": "price",
        "missing_values": {col: int(df[col].isna().sum()) for col in df.columns},
        "duplicates": int(df.duplicated().sum()),
        "price_stats": {
            "min": round(float(df["price"].min()), 2),
            "max": round(float(df["price"].max()), 2),
            "mean": round(float(df["price"].mean()), 2),
            "median": round(float(df["price"].median()), 2),
            "std": round(float(df["price"].std()), 2),
        },
        "numeric_summary": {
            col: {
                "min": round(float(numeric[col].min()), 2),
                "max": round(float(numeric[col].max()), 2),
                "mean": round(float(numeric[col].mean()), 2),
            }
            for col in numeric.columns
            if col != "price"
        },
    }


def price_distribution(df: pd.DataFrame, bins: int = 12) -> list[dict]:
    counts, edges = pd.cut(df["price"], bins=bins, retbins=True)
    grouped = counts.value_counts().sort_index()
    return [
        {
            "range": f"{int(interval.left):,}–{int(interval.right):,}",
            "count": int(count),
        }
        for interval, count in grouped.items()
    ]


def categorical_breakdown(df: pd.DataFrame, column: str, top_n: int = 8) -> list[dict]:
    counts = df[column].value_counts().head(top_n)
    return [{"label": str(idx), "count": int(val)} for idx, val in counts.items()]


def correlation_matrix(df: pd.DataFrame) -> list[dict]:
    numeric = df[["duration", "days_left", "price"]].corr()
    pairs: list[dict] = []
    cols = list(numeric.columns)
    for i, a in enumerate(cols):
        for b in cols[i + 1 :]:
            pairs.append({"feature_a": a, "feature_b": b, "correlation": round(float(numeric.loc[a, b]), 3)})
    return pairs


def scatter_sample(df: pd.DataFrame, x: str, y: str = "price", limit: int = 80) -> list[dict]:
    sample = df[[x, y]].sample(n=min(limit, len(df)), random_state=42)
    return [{"x": round(float(row[x]), 2), "y": round(float(row[y]), 2)} for _, row in sample.iterrows()]


def class_price_comparison(df: pd.DataFrame) -> list[dict]:
    grouped = df.groupby("class")["price"].mean().sort_values(ascending=False)
    return [{"label": str(idx), "avg_price": round(float(val), 2)} for idx, val in grouped.items()]


def build_eda_report(df: pd.DataFrame) -> dict:
    class_col = "class" if "class" in df.columns else "travel_class"
    return {
        "overview": dataset_overview(df),
        "price_distribution": price_distribution(df),
        "airline_counts": categorical_breakdown(df, "airline"),
        "route_counts": categorical_breakdown(df, "source_city"),
        "class_avg_price": class_price_comparison(df),
        "correlations": correlation_matrix(df),
        "duration_vs_price": scatter_sample(df, "duration"),
        "days_left_vs_price": scatter_sample(df, "days_left"),
        "stops_breakdown": categorical_breakdown(df, "stops", top_n=5),
        "class_breakdown": categorical_breakdown(df, class_col, top_n=5),
    }
