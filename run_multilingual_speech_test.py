
import csv
import json
from pathlib import Path

from src.intent_classifier import classify_intent
from src.speech_recognizer import SpeechRecognizer
from src.speech_evaluator import evaluate_transcription


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "speech_test_data.json"
REPORT_FILE = BASE_DIR / "reports" / "multilingual_speech_report.csv"


def main():
    with DATA_FILE.open("r", encoding="utf-8") as file:
        test_cases = json.load(file)

    recognizer = SpeechRecognizer()
    results = []

    for case in test_cases:
        test_id = case["test_id"]
        audio_path = BASE_DIR / case["audio_file"]

        if not audio_path.is_file():
            print(f"[SKIP] {test_id}: Audio file not found")
            results.append({
                "test_id": test_id,
                "locale": case["locale"],
                "reference": case["reference"],
                "recognized": "",
                "wer": "",
                "cer": "",
                "expected_intent": case["expected_intent"],
                "actual_intent": "",
                "status": "SKIP",
            })
            continue

        try:
            transcription = recognizer.transcribe(
                str(audio_path),
                language=case["language"],
            )

            recognized = transcription["text"]
            metrics = evaluate_transcription(
                case["reference"],
                recognized,
            )

            expected_intent = case["expected_intent"]
            actual_intent = classify_intent(recognized)

            status = (
                "PASS"
                if metrics["wer"] == 0.0
                and actual_intent == expected_intent
                else "FAIL"
            )

            results.append({
                "test_id": test_id,
                "locale": case["locale"],
                "reference": case["reference"],
                "recognized": recognized,
                "wer": round(metrics["wer"], 4),
                "cer": round(metrics["cer"], 4),
                "expected_intent": expected_intent,
                "actual_intent": actual_intent,
                "status": status,
            })

            print(
                f"[{status}] {test_id} | "
                f"WER={metrics['wer']:.4f} | "
                f"CER={metrics['cer']:.4f} | "
                f"Intent={actual_intent}"
            )

        except Exception as error:
            print(f"[ERROR] {test_id}: {error}")
            results.append({
                "test_id": test_id,
                "locale": case["locale"],
                "reference": case["reference"],
                "recognized": "",
                "wer": "",
                "cer": "",
                "expected_intent": case["expected_intent"],
                "actual_intent": "",
                "status": "ERROR",
            })

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "test_id",
        "locale",
        "reference",
        "recognized",
        "wer",
        "cer",
        "expected_intent",
        "actual_intent",
        "status",
    ]

    with REPORT_FILE.open(
        "w", newline="", encoding="utf-8-sig"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    passed = sum(r["status"] == "PASS" for r in results)
    failed = sum(r["status"] == "FAIL" for r in results)
    skipped = sum(r["status"] == "SKIP" for r in results)
    errors = sum(r["status"] == "ERROR" for r in results)

    print("\n=== Multilingual Speech QA Summary ===")
    print(f"Total:   {len(results)}")
    print(f"Passed:  {passed}")
    print(f"Failed:  {failed}")
    print(f"Skipped: {skipped}")
    print(f"Errors:  {errors}")
    print(f"Report:  {REPORT_FILE}")

    if failed or skipped or errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
