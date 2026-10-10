
import csv
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
BASELINE_FILE = BASE_DIR / "data" / "speech_performance_baseline.json"
BENCHMARK_FILE = BASE_DIR / "reports" / "speech_benchmark_report.csv"
REGRESSION_REPORT = BASE_DIR / "reports" / "performance_regression_report.csv"

METRICS = [
    "avg_latency_seconds",
    "p95_latency_seconds",
]


def calculate_regression_percent(baseline, current):
    if baseline <= 0:
        raise ValueError("Baseline must be greater than zero")

    return (current - baseline) / baseline * 100


def main():
    with BASELINE_FILE.open("r", encoding="utf-8") as file:
        baseline_data = json.load(file)

    with BENCHMARK_FILE.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        benchmark_results = list(csv.DictReader(file))

    baselines = baseline_data["baselines"]
    threshold = float(baseline_data["max_regression_percent"])

    results = []
    failed = False
    seen_ids = set()

    for benchmark in benchmark_results:
        test_id = benchmark["test_id"]

        if test_id in seen_ids:
            raise ValueError(f"Duplicate test ID: {test_id}")

        seen_ids.add(test_id)

        if test_id not in baselines:
            raise ValueError(f"Missing baseline for: {test_id}")

        baseline = baselines[test_id]

        if benchmark["locale"] != baseline["locale"]:
            raise ValueError(f"Locale mismatch: {test_id}")

        for metric in METRICS:
            baseline_value = float(baseline[metric])
            current_value = float(benchmark[metric])

            regression_percent = calculate_regression_percent(
                baseline_value,
                current_value,
            )

            status = (
                "FAIL"
                if regression_percent > threshold
                else "PASS"
            )

            if status == "FAIL":
                failed = True

            results.append({
                "test_id": test_id,
                "locale": benchmark["locale"],
                "metric": metric,
                "baseline": round(baseline_value, 4),
                "current": round(current_value, 4),
                "regression_percent": round(regression_percent, 2),
                "threshold_percent": threshold,
                "status": status,
            })

            print(
                f"[{status}] {test_id} | {metric} | "
                f"Baseline={baseline_value:.4f}s | "
                f"Current={current_value:.4f}s | "
                f"Change={regression_percent:+.2f}%"
            )

    missing_ids = set(baselines) - seen_ids

    if missing_ids:
        raise ValueError(
            f"Missing benchmark results for: {sorted(missing_ids)}"
        )

    REGRESSION_REPORT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "test_id",
        "locale",
        "metric",
        "baseline",
        "current",
        "regression_percent",
        "threshold_percent",
        "status",
    ]

    with REGRESSION_REPORT.open(
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print("\n=== Performance Regression Summary ===")
    print(f"Metrics checked: {len(results)}")
    print(f"Threshold: +{threshold:.1f}%")
    print(f"Report: {REGRESSION_REPORT}")

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
