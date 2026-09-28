"""Étape « Préparer » : découpage train / test stratifié (data/processed)."""
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

INTERIM_PATH = Path("data/interim/reviews_clean.parquet")
PROCESSED_DIR = Path("data/processed")
TEST_SIZE = 0.2
SEED = 42


def split(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    return train_test_split(df, test_size=TEST_SIZE, stratify=df["label"], random_state=SEED)


def main() -> None:
    train, test = split(pd.read_parquet(INTERIM_PATH))
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    train.to_parquet(PROCESSED_DIR / "train.parquet", index=False)
    test.to_parquet(PROCESSED_DIR / "test.parquet", index=False)
    print(f"train : {len(train)} | test : {len(test)}")


if __name__ == "__main__":
    main()
