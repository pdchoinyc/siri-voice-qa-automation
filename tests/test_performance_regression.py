
import csv
import json
from pathlib import Path

import pytest

from run_performance_regression import calculate_regression_percent


BASE_DIR = Path(__file__).resolve().parents[1]

BASELINE_FILE = (
    BASE_DIR / "data" / "speech_performance_baseline.json"
)

BENCHMARK_FILE = (
    BASE_DIR / "reports" / "speech_benchmark_report.csv"
)


@pytest.mark.performance
def test_performance_regression():
    assert BASELINE_FILE.is_file(), "Baseline file is missing"

    if not BENCHMARK_FILE.is_file():
        pytest.skip("Local benchmark report is unavailable")

    with BASELINE_FILE.open("r", encoding="utf-8") as file:
        config = json.load(file)

    with BENCHMARK_FILE.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        results = list(csv.DictReader(file))

    baselines = config["baselines"]
    threshold = float(config["max_regression_percent"])

    assert len(results) == len(baselines), (
        "Benchmark case count does not match baseline"
    )

    seen_ids = set()

    for result in results:
        test_id = result["test_id"]

        assert test_id not in seen_ids, (
            f"Duplicate test ID: {test_id}"
        )
        seen_ids.add(test_id)

        assert test_id in baselines, (
            f"Missing baseline: {test_id}"
        )

        baseline = baselines[test_id]

        assert result["locale"] == baseline["locale"], (
            f"Locale mismatch: {test_id}"
        )

        for metric in (
            "avg_latency_seconds",
            "p95_latency_seconds",
        ):
            change = calculate_regression_percent(
                float(baseline[metric]),
                float(result[metric]),
            )

            assert change <= threshold, (
                f"{test_id} {metric}: "
                f"Regression +{change:.2f}% "
                f"exceeds {threshold:.1f}%"
            )

    assert seen_ids == set(baselines)
