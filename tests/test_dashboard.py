
import json

import pytest

from generate_dashboard import create_dashboard


@pytest.fixture
def sample_report(tmp_path):
    report = {
        "generated_at": "2026-10-11T00:00:00+00:00",
        "pytest": {
            "status": "PASS",
            "total": 48,
            "passed": 48,
        },
        "speech_benchmark": {
            "status": "AVAILABLE",
            "sample_count": 1,
            "results": [
                {
                    "locale": "ko-KR",
                    "avg_latency_seconds": "0.55",
                    "p95_latency_seconds": "0.60",
                    "avg_wer": "0.0",
                    "avg_cer": "0.0",
                    "intent_accuracy": "1.0",
                }
            ],
        },
        "performance_regression": {
            "status": "PASS",
            "total_metrics": 1,
            "passed": 1,
            "results": [
                {
                    "locale": "ko-KR",
                    "metric": "avg_latency_seconds",
                    "regression_percent": "0.0",
                    "status": "PASS",
                }
            ],
        },
    }

    path = tmp_path / "qa_summary.json"
    path.write_text(json.dumps(report), encoding="utf-8")
    return path


def test_dashboard_file_is_created(sample_report, tmp_path):
    output = tmp_path / "dashboard.html"

    create_dashboard(sample_report, output)

    assert output.is_file()


def test_dashboard_contains_qa_results(sample_report, tmp_path):
    output = tmp_path / "dashboard.html"

    create_dashboard(sample_report, output)

    html = output.read_text(encoding="utf-8")

    assert "Multilingual Voice QA Dashboard" in html
    assert "48 / 48" in html
    assert "ko-KR" in html
    assert "Performance Regression" in html


def test_dashboard_missing_summary_raises_error(tmp_path):
    missing_file = tmp_path / "missing.json"
    output = tmp_path / "dashboard.html"

    with pytest.raises(FileNotFoundError):
        create_dashboard(missing_file, output)

    assert not output.exists()
