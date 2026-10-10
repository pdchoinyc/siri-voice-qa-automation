
import csv
import json
import math
import statistics
import time
from pathlib import Path

from src.intent_classifier import classify_intent
from src.speech_evaluator import evaluate_transcription
from src.speech_recognizer import SpeechRecognizer


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "speech_test_data.json"
REPORT_FILE = BASE_DIR / "reports" / "speech_benchmark_report.csv"

ITERATIONS = 10


def percentile(values, percentile_value):
    """Calculate percentile using the nearest-rank method."""
    sorted_values = sorted(values)
    index = max(0, math.ceil(percentile_value / 100 * len(values)) - 1)
    return sorted_values[index]


def get_audio_duration(audio_path):
    """Read audio duration without loading the full audio into memory."""
    import av

    with av.open(str(audio_path)) as container:
        audio_streams = [
            stream for stream in container.streams
            if stream.type == "audio"
        ]

        if not audio_streams:
            raise ValueError(f"No audio stream found: {audio_path}")

        stream = audio_streams[0]

        if stream.duration is not None and stream.time_base is not None:
            return float(stream.duration * stream.time_base)

        if container.duration is not None:
            return container.duration / 1_000_000

        raise ValueError(f"Audio duration unavailable: {audio_path}")


def main():
    with DATA_FILE.open("r", encoding="utf-8") as file:
        test_cases = json.load(file)

    recognizer = SpeechRecognizer()
    results = []

    for case in test_cases:
        audio_path = BASE_DIR / case["audio_file"]
        test_id = case["test_id"]

        if not audio_path.is_file():
            print(f"[SKIP] {test_id}: Audio file not found")
            continue

        audio_duration = get_audio_duration(audio_path)

        if audio_duration <= 0:
            raise ValueError(f"Invalid audio duration: {audio_path}")

        print(f"\n=== Benchmark: {test_id} ===")
        print(f"Audio duration: {audio_duration:.3f}s")

        # Warm-up run is excluded from the measured iterations.
        recognizer.transcribe(
            str(audio_path),
            language=case["language"],
        )

        latencies = []
        rtfs = []
        wers = []
        cers = []
        intent_matches = []

        for iteration in range(1, ITERATIONS + 1):
            start = time.perf_counter()

            transcription = recognizer.transcribe(
                str(audio_path),
                language=case["language"],
            )

            latency = time.perf_counter() - start
            rtf = latency / audio_duration

            recognized = transcription["text"]
            metrics = evaluate_transcription(
                case["reference"],
                recognized,
            )
            actual_intent = classify_intent(recognized)

            latencies.append(latency)
            rtfs.append(rtf)
            wers.append(metrics["wer"])
            cers.append(metrics["cer"])
            intent_matches.append(
                actual_intent == case["expected_intent"]
            )

            print(
                f"Run {iteration:02d}/{ITERATIONS} | "
                f"Latency={latency:.3f}s | "
                f"RTF={rtf:.3f} | "
                f"WER={metrics['wer']:.3f} | "
                f"CER={metrics['cer']:.3f} | "
                f"Intent={actual_intent}"
            )

        avg_latency = statistics.mean(latencies)
        p95_latency = percentile(latencies, 95)

        result = {
            "test_id": test_id,
            "locale": case["locale"],
            "iterations": ITERATIONS,
            "audio_duration_seconds": round(audio_duration, 4),
            "avg_latency_seconds": round(avg_latency, 4),
            "min_latency_seconds": round(min(latencies), 4),
            "max_latency_seconds": round(max(latencies), 4),
            "p95_latency_seconds": round(p95_latency, 4),
            "stddev_latency_seconds": round(
                statistics.stdev(latencies), 4
            ),
            "avg_rtf": round(statistics.mean(rtfs), 4),
            "avg_wer": round(statistics.mean(wers), 4),
            "avg_cer": round(statistics.mean(cers), 4),
            "intent_accuracy": round(
                sum(intent_matches) / ITERATIONS, 4
            ),
        }

        results.append(result)

        print(
            f"[SUMMARY] {test_id} | "
            f"AVG={avg_latency:.3f}s | "
            f"P95={p95_latency:.3f}s | "
            f"AVG RTF={result['avg_rtf']:.3f}"
        )

    if not results:
        raise SystemExit("No audio samples available for benchmarking.")

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = list(results[0].keys())

    with REPORT_FILE.open(
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print("\n=== Speech Benchmark Completed ===")
    print(f"Test cases: {len(results)}")
    print(f"Iterations per case: {ITERATIONS}")
    print(f"Report: {REPORT_FILE}")


if __name__ == "__main__":
    main()
