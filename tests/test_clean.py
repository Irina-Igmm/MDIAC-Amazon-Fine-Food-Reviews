import pandas as pd

from src.data.clean import clean, clean_text, score_to_label


def test_clean_text_removes_html_and_punctuation():
    assert clean_text("Great <br />product!!  Loved it.") == "great product loved it"


def test_score_to_label():
    assert score_to_label(5) == 1
    assert score_to_label(4) == 1
    assert score_to_label(3) is None
    assert score_to_label(1) == 0


def test_clean_drops_neutral_duplicates_and_bad_helpfulness():
    df = pd.DataFrame({
        "Id": [1, 2, 3, 4],
        "UserId": ["a", "a", "b", "c"],
        "ProfileName": ["A", "A", "B", "C"],
        "Time": [1, 1, 2, 3],
        "Text": ["Good!", "Good!", "Meh", "Bad"],
        "Score": [5, 5, 3, 1],
        "HelpfulnessNumerator": [0, 0, 0, 3],
        "HelpfulnessDenominator": [0, 0, 0, 1],
    })
    out = clean(df)
    assert out["Id"].tolist() == [1]
    assert out["label"].tolist() == [1]
