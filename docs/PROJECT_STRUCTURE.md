# Project Structure

```
airfare/
├── backend/                         # FastAPI + SQL + ML pipeline
│   ├── app/                         # Application layer
│   │   ├── api/v1/
│   │   │   ├── router.py
│   │   │   └── endpoints/
│   │   │       ├── health.py        # Health + form options
│   │   │       ├── analytics.py     # Problem, EDA, features
│   │   │       ├── training.py      # Train + metrics
│   │   │       └── predict.py       # Fare prediction
│   │   ├── core/config.py
│   │   ├── db/                      # SQLAlchemy models + session
│   │   ├── schemas/                 # Pydantic request/response models
│   │   ├── services/                # Business logic orchestration
│   │   └── main.py
│   ├── ml/                          # Machine learning (separate from API)
│   │   ├── constants.py
│   │   ├── eda/analyzer.py
│   │   ├── preprocessing/
│   │   │   ├── dataset.py
│   │   │   └── pipeline.py
│   │   ├── training/trainer.py
│   │   ├── evaluation/selection.py
│   │   └── prediction/inference.py
│   ├── scripts/train_models.py
│   ├── data/                        # Optional raw datasets
│   ├── models/                      # Saved .joblib artifacts
│   ├── artifacts/                   # Metadata + selection results
│   └── requirements.txt
│
├── frontend/                        # Vite + React + TypeScript
│   └── src/
│       ├── api/client.ts
│       ├── config/navigation.ts     # ML pipeline routes
│       ├── components/
│       │   ├── layout/              # App shell + sidebar
│       │   ├── common/              # Shared UI blocks
│       │   ├── charts/              # Bar + scatter (vanilla CSS/SVG)
│       │   └── predict/             # Prediction form + results
│       └── pages/
│           ├── problem/             # Step 1
│           ├── eda/                   # Step 2
│           ├── features/            # Step 3
│           ├── models/              # Step 4
│           ├── predict/             # Step 5
│           └── deployment/          # Step 6
│
└── docs/
```

## ML workflow mapping

| Step | Frontend route   | Backend endpoint              |
|------|------------------|-------------------------------|
| 1    | `/problem`       | `GET /api/analytics/problem`  |
| 2    | `/eda`           | `GET /api/analytics/eda`      |
| 3    | `/features`      | `GET /api/analytics/features` |
| 4    | `/models`        | `GET /api/metrics`, `POST /api/train` |
| 5    | `/predict`       | `POST /api/predict`           |
| 6    | `/deployment`    | Documentation (static)        |
