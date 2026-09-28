"""Étape « Tester » : évaluation du modèle sur le jeu de test."""
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix

TEST_PATH = Path("data/processed/test.parquet")
MODEL_PATH = Path("models/model.joblib")


def main() -> None:
    test = pd.read_parquet(TEST_PATH)
    model = joblib.load(MODEL_PATH)
    preds = model.predict(test["text"])
    print(classification_report(test["label"], preds, target_names=["négatif", "positif"]))
    print("Matrice de confusion :")
    print(confusion_matrix(test["label"], preds))


if __name__ == "__main__":
    main()
