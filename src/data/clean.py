"""Étape « Nettoyer » : Reviews.csv brut -> données nettoyées (data/interim)."""
import re
from pathlib import Path

import pandas as pd

RAW_PATH = Path("data/raw/Reviews.csv")
INTERIM_PATH = Path("data/interim/reviews_clean.parquet")

_HTML_TAG = re.compile(r"<[^>]+>")
_NON_ALNUM = re.compile(r"[^a-z0-9\s]")
_SPACES = re.compile(r"\s+")


def clean_text(text: str) -> str:
    """Minuscules, suppression des balises HTML, ponctuation et espaces multiples."""
    text = _HTML_TAG.sub(" ", str(text).lower())
    text = _NON_ALNUM.sub(" ", text)
    return _SPACES.sub(" ", text).strip()


def score_to_label(score: int) -> int | None:
    """4-5 -> 1 (positif), 1-2 -> 0 (négatif), 3 -> None (neutre, écarté)."""
    if score >= 4:
        return 1
    if score <= 2:
        return 0
    return None


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(subset=["Text", "Score"])
    df = df.drop_duplicates(subset=["UserId", "ProfileName", "Time", "Text"])
    df = df[df["HelpfulnessNumerator"] <= df["HelpfulnessDenominator"]]
    df = df.assign(label=df["Score"].map(score_to_label)).dropna(subset=["label"])
    df = df.assign(text=df["Text"].map(clean_text), label=df["label"].astype(int))
    df = df[df["text"] != ""]
    return df[["Id", "text", "label"]].reset_index(drop=True)


def main() -> None:
    df = pd.read_csv(RAW_PATH)
    cleaned = clean(df)
    INTERIM_PATH.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_parquet(INTERIM_PATH, index=False)
    print(f"{len(df)} lignes brutes -> {len(cleaned)} lignes nettoyées : {INTERIM_PATH}")


if __name__ == "__main__":
    main()
