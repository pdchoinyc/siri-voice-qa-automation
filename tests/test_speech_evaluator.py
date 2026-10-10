import pytest

from src.speech_evaluator import (
    normalize_text,
    evaluate_transcription,
)


@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("오늘 날씨 알려줘.", "오늘 날씨 알려줘"),
        ("HELLO WORLD!", "hello world"),
        ("  Set   a Timer  ", "set a timer"),
        ("今日の天気を教えて。", "今日の天気を教えて"),
    ],
)
def test_normalize_text(input_text, expected):
    assert normalize_text(input_text) == expected


def test_punctuation_does_not_affect_error_rate():
    result = evaluate_transcription(
        "오늘 날씨 알려줘",
        "오늘 날씨 알려줘."
    )

    assert result["wer"] == 0.0
    assert result["cer"] == 0.0


def test_actual_word_error():
    result = evaluate_transcription(
        "오늘 날씨 알려줘",
        "오늘 시간 알려줘"
    )

    assert result["wer"] > 0.0
    assert result["cer"] > 0.0