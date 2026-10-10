
import json
import time
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

    # Measure STT inference time
    start_time = time.perf_counter()

    result = recognizer.transcribe(
        str(audio_path),
        language=case["language"],
    )

    latency = time.perf_counter() - start_time

    recognized = result["text"]

    metrics = evaluate_transcription(
        case["reference"],
        recognized,
    )

    actual_intent = classify_intent(recognized)

    # Display QA metrics in pytest output
    print(f"\nTest ID: {case['test_id']}")
    print(f"Locale: {case['locale']}")
    print(f"Reference: {case['reference']}")
    print(f"Recognized: {recognized}")
    print(f"WER: {metrics['wer']:.4f}")
    print(f"CER: {metrics['cer']:.4f}")
    print(f"Latency: {latency:.3f}s")
    print(f"Intent: {actual_intent}")

    # Accuracy and performance assertions
    assert metrics["wer"] <= case["max_wer"], (
        f"WER exceeded threshold: "
        f"{metrics['wer']:.4f} > {case['max_wer']}"
    )

    assert metrics["cer"] <= case["max_cer"], (
        f"CER exceeded threshold: "
        f"{metrics['cer']:.4f} > {case['max_cer']}"
    )

    assert latency <= case["max_latency_seconds"], (
        f"Latency exceeded threshold: "
        f"{latency:.3f}s > {case['max_latency_seconds']}s"
    )

    assert actual_intent == case["expected_intent"], (
        f"Intent mismatch: "
        f"Expected={case['expected_intent']}, "
        f"Actual={actual_intent}"
    )
