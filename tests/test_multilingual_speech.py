
import json
from pathlib import Path

import pytest

from src.intent_classifier import classify_intent
from src.speech_evaluator import evaluate_transcription
from src.speech_recognizer import SpeechRecognizer


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "speech_test_data.json"


def load_test_cases():
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture(scope="module")
def recognizer():
    return SpeechRecognizer()


@pytest.mark.speech
@pytest.mark.parametrize(
    "case",
    load_test_cases(),
    ids=lambda case: case["test_id"],
)
def test_multilingual_speech(case, recognizer):
    audio_path = BASE_DIR / case["audio_file"]

    if not audio_path.is_file():
        pytest.skip(f"Audio file not found: {audio_path}")

    result = recognizer.transcribe(
        str(audio_path),
        language=case["language"],
    )

    recognized = result["text"]

    metrics = evaluate_transcription(
        case["reference"],
        recognized,
    )

    actual_intent = classify_intent(recognized)

    assert metrics["wer"] == 0.0, (
        f"{case['test_id']}: WER={metrics['wer']}, "
        f"Expected={case['reference']}, "
        f"Actual={recognized}"
    )

    assert actual_intent == case["expected_intent"], (
        f"{case['test_id']}: "
        f"Expected intent={case['expected_intent']}, "
        f"Actual intent={actual_intent}"
    )
