# Airline Fare Prediction — Project Context

This document describes the ML workflow and architecture. The **web app** stays simple (Predict · Models · About); this is reference context for your report or viva.

---

## 1. Problem understanding

| Item | Detail |
|------|--------|
| **Goal** | Predict domestic flight ticket price (INR) from route and booking features |
| **Type** | Supervised regression |
| **Target** | `price` |
| **Input features** | airline, source/destination city, departure/arrival time bucket, stops, class, duration, days_left |
| **Success metrics** | RMSE, MAE, R² (lower RMSE / higher R² is better) |

**Algorithms used**

- Linear Regression  
- Random Forest Regression  
- Decision Tree Regression  
- XGBoost Regression  

Best model is chosen by **lowest RMSE** on the hold-out test set.

---

## 2. Data & EDA

- Training data is stored in **SQL** (`flight_records` table, SQLite by default).
- On first run, ~2,500 synthetic flight rows are seeded if the table is small.
- EDA (exploratory analysis) covers:
  - Row/column counts, missing values, duplicates  
  - Price distribution (min, max, mean, median, std)  
  - Counts by airline, city, stops, class  
  - Correlations between `duration`, `days_left`, and `price`  

Backend helper: `backend/ml/eda/analyzer.py`  
Optional API: `GET /api/analytics/eda`

---

## 3. Feature engineering

| Type | Columns | Transform |
|------|---------|-----------|
| Categorical | airline, cities, times, stops, class | `OneHotEncoder` (unknown categories ignored at predict time) |
| Numeric | duration, days_left | `StandardScaler` |

Pipeline (scikit-learn):

```
ColumnTransformer → Regressor (one of four models)
```

Code: `backend/ml/preprocessing/pipeline.py`

---

## 4. Model training & evaluation

1. 80/20 train/test split (`random_state=42`)  
2. Train all four regressors with the same preprocessor  
3. Evaluate RMSE, MAE, R² on test set  
4. Save all `.joblib` artifacts to `backend/models/`  
5. Persist metrics to SQL (`model_metrics` table)  

Code:

- Training: `backend/ml/training/trainer.py`  
- Selection: `backend/ml/evaluation/selection.py`  

CLI: `python -m scripts.train_models`  
API: `POST /api/train`, `GET /api/metrics`

---

## 5. UI (frontend)

Simple **FareCast** app (Vite + React + TypeScript):

| Page | Purpose |
|------|---------|
| **Predict** | Form → `POST /api/predict` → single predicted fare (best model) |
| **Models** | View metrics, retrain |
| **About** | Stack and API summary |

Not a multi-step pipeline wizard — just prediction and model management.

---

## 6. Deployment

**Local development**

```bash
# Backend
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Frontend
cd frontend
npm run dev
```

- API docs: http://127.0.0.1:8000/docs  
- App: http://localhost:5173 (Vite proxies `/api` to backend)

**Production notes**

- Use PostgreSQL via `DATABASE_URL`  
- Set `CORS_ORIGINS` to your frontend URL  
- `npm run build` → serve `frontend/dist/`  
- Run API with Gunicorn + Uvicorn workers  
- Keep `backend/models/` on persistent storage  

---

## Folder structure (backend)

```
backend/
├── app/                 # FastAPI, DB, services, API routes
├── ml/
│   ├── eda/
│   ├── preprocessing/
│   ├── training/
│   ├── evaluation/
│   └── prediction/
├── scripts/
├── data/
├── models/              # Trained .joblib files
└── artifacts/           # Metadata, best model marker
```

See also [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md).
