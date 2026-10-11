
import pytest

from run_performance_regression import validate_benchmark_data


BASELINES = {
    "STT-KO-001": {
        "locale": "ko-KR",
        "avg_latency_seconds": 0.5,
        "p95_latency_seconds": 0.7,
    }
}


def valid_result():
    return {
        "test_id": "STT-KO-001",
        "locale": "ko-KR",
        "avg_latency_seconds": "0.6",
        "p95_latency_seconds": "0.8",
    }


def test_duplicate_test_id():
    rows = [valid_result(), valid_result()]

    with pytest.raises(ValueError, match="Duplicate test ID"):
        validate_benchmark_data(rows, BASELINES)


def test_missing_baseline():
    row = valid_result()
    row["test_id"] = "STT-UNKNOWN"

    with pytest.raises(ValueError, match="Missing baseline"):
        validate_benchmark_data([row], BASELINES)


def test_missing_benchmark_result():
    with pytest.raises(ValueError, match="Missing benchmark results"):
        validate_benchmark_data([], BASELINES)


def test_invalid_metric_value():
    row = valid_result()
    row["avg_latency_seconds"] = "invalid"

    with pytest.raises(ValueError, match="Invalid metric data"):
        validate_benchmark_data([row], BASELINES)
