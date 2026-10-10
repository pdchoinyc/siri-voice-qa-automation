import pytest

from src.intent_classifier import classify_intent


@pytest.mark.parametrize(
    "utterance, expected",
    [
        ("What's the weather today?", "WEATHER"),
        ("오늘 날씨 알려줘", "WEATHER"),
        ("Set a timer for 5 minutes", "TIMER"),
        ("5분 타이머 설정해줘", "TIMER"),
        ("Set an alarm", "ALARM"),
        ("내일 아침 알람 설정해줘", "ALARM"),
        ("Play some music", "UNKNOWN"),
    ],
)
def test_intent_classification(utterance, expected):
    actual = classify_intent(utterance)

    assert actual == expected