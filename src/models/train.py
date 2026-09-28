"""Étape « Créer le modèle » : TF-IDF + régression logistique."""
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

TRAIN_PATH = Path("data/processed/train.parquet")
MODEL_PATH = Path("models/model.joblib")


def build_pipeline() -> Pipeline:
    return Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=5, max_features=200_000)),
        ("clf", LogisticRegression(max_iter=1000, class_weight="balanced")),
    ])


def main() -> None:
    train = pd.read_parquet(TRAIN_PATH)
    model = build_pipeline().fit(train["text"], train["label"])
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Modèle sauvegardé : {MODEL_PATH}")


if __name__ == "__main__":
    main()
