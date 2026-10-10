import json
from pathlib import Path

import pytest

from src.intent_classifier import classify_intent


DATA_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "intent_test_data.json"
)


def load_test_data():
    with DATA_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


test_data = load_test_data()


@pytest.mark.parametrize(
    "case",
    test_data,
    ids=[case["id"] for case in test_data],
)
def test_multilingual_intent(case):
    actual_intent = classify_intent(case["utterance"])

    assert actual_intent == case["expected_intent"], (
        f"Test ID: {case['id']}, "
        f"Locale: {case['locale']}, "
        f"Expected: {case['expected_intent']}, "
        f"Actual: {actual_intent}"
    )