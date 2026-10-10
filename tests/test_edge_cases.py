import pytest

from src.intent_classifier import classify_intent


@pytest.mark.parametrize(
    "utterance, expected",
    [
        ("", "UNKNOWN"),
        ("   ", "UNKNOWN"),
        ("Play some music", "UNKNOWN"),
        ("Hello Siri", "UNKNOWN"),
        ("WEATHER", "WEATHER"),
        ("TiMeR", "TIMER"),
        ("ALARM", "ALARM"),
        ("오늘 날씨!!!", "WEATHER"),
        ("タイマー！", "TIMER"),
        ("weatherproof jacket", "UNKNOWN"),
        ("timer123", "UNKNOWN"),
        ("a" * 10000, "UNKNOWN"),
    ],
)
def test_edge_cases(utterance, expected):
    actual = classify_intent(utterance)
    assert actual == expected


@pytest.mark.parametrize(
    "invalid_input",
    [None, 123, [], {}],
)
def test_invalid_input_types(invalid_input):
    with pytest.raises(TypeError):
        classify_intent(invalid_input)


@pytest.mark.parametrize(
    "utterance",
    [
        "Set a timer and check the weather",
        "날씨 알려주고 타이머 설정해줘",
    ],
)
def test_multiple_intents(utterance):
    assert classify_intent(utterance) == "MULTIPLE_INTENTS"