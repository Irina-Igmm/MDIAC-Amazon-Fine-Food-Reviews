"""Étape « Surveiller » : compare les données de production aux données d'entraînement.

Usage : python -m monitoring.drift
"""
import json
from pathlib import Path

import pandas as pd

TRAIN_PATH = Path("data/processed/train.parquet")
PREDICTION_LOG = Path("monitoring/logs/predictions.jsonl")
REPORT_DIR = Path("monitoring/reports")


def load_predictions() -> pd.DataFrame:
    with PREDICTION_LOG.open(encoding="utf-8") as f:
        return pd.DataFrame([json.loads(line) for line in f])


def summary(train: pd.DataFrame, prod: pd.DataFrame) -> dict:
    """Indicateurs simples de drift : longueur des textes et part de positifs."""
    return {
        "train_len_moy": float(train["text"].str.split().str.len().mean()),
        "prod_len_moy": float(prod["text"].str.split().str.len().mean()),
        "train_part_positifs": float(train["label"].mean()),
        "prod_part_positifs": float(prod["label"].mean()),
        "n_predictions": len(prod),
    }


def main() -> None:
    report = summary(pd.read_parquet(TRAIN_PATH), load_predictions())
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "drift_summary.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
