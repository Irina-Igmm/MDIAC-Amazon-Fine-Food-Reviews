"""Étape « Mettre en ligne » : API FastAPI de prédiction de sentiment."""
import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.data.clean import clean_text

MODEL_PATH = Path("models/model.joblib")
PREDICTION_LOG = Path("monitoring/logs/predictions.jsonl")

app = FastAPI(title="Amazon Fine Food Reviews – Sentiment API")
_model = None


def get_model():
    global _model
    if _model is None:
        if not MODEL_PATH.exists():
            raise HTTPException(status_code=503, detail="Modèle non entraîné")
        _model = joblib.load(MODEL_PATH)
    return _model


class Review(BaseModel):
    text: str


class Prediction(BaseModel):
    label: int
    sentiment: str
    proba_positive: float


def log_prediction(text: str, pred: Prediction) -> None:
    """Journalise chaque prédiction pour l'étape « Surveiller »."""
    PREDICTION_LOG.parent.mkdir(parents=True, exist_ok=True)
    record = {"ts": datetime.now(timezone.utc).isoformat(), "text": text, **pred.model_dump()}
    with PREDICTION_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "model_loaded": MODEL_PATH.exists()}


@app.post("/predict", response_model=Prediction)
def predict(review: Review) -> Prediction:
    model = get_model()
    proba = float(model.predict_proba([clean_text(review.text)])[0][1])
    label = int(proba >= 0.5)
    pred = Prediction(label=label, sentiment="positif" if label else "négatif", proba_positive=proba)
    log_prediction(review.text, pred)
    return pred
