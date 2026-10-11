
import csv
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"

BENCHMARK_FILE = REPORT_DIR / "speech_benchmark_report.csv"
REGRESSION_FILE = REPORT_DIR / "performance_regression_report.csv"
OUTPUT_FILE = REPORT_DIR / "qa_summary.json"


def read_csv(file_path):
    if not file_path.is_file():
        return None

    with file_path.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        return list(csv.DictReader(file))


def read_pytest_results():
    xml_file = REPORT_DIR / "pytest_results.xml"

    if not xml_file.is_file():
        return {
            "status": "NOT_RUN",
            "total": 0,
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "skipped": 0,
        }

    root = ET.parse(xml_file).getroot()

    suites = (
        [root]
        if root.tag == "testsuite"
        else root.findall(".//testsuite")
    )

    # Aggregate testcase elements rather than suite attributes
    # to avoid double-counting nested test suites.
    cases = root.findall(".//testcase")

    total = len(cases)
    failed = sum(
        case.find("failure") is not None
        for case in cases
    )
    errors = sum(
        case.find("error") is not None
        for case in cases
    )
    skipped = sum(
        case.find("skipped") is not None
        for case in cases
    )
    passed = total - failed - errors - skipped

    return {
        "status": (
            "FAIL"
            if failed or errors
            else "PASS"
            if total > 0
            else "INCOMPLETE"
        ),
        "total": total,
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "skipped": skipped,
    }

def create_qa_report():
    benchmark = read_csv(BENCHMARK_FILE)
    regression = read_csv(REGRESSION_FILE)

    report = {
        "project": "Multilingual Voice QA Automation",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pytest": read_pytest_results(),
        "speech_benchmark": {
            "status": "NOT_RUN" if benchmark is None else "AVAILABLE",
            "sample_count": 0 if benchmark is None else len(benchmark),
            "results": [] if benchmark is None else benchmark,
        },
        "performance_regression": {
            "status": "NOT_RUN",
            "total_metrics": 0,
            "passed": 0,
            "failed": 0,
            "results": [],
        },
    }

    if regression is not None:
        statuses = [row.get("status") for row in regression]

        passed = statuses.count("PASS")
        failed = statuses.count("FAIL")

        report["performance_regression"] = {
            "status": (
                "FAIL"
                if failed > 0
                else "PASS"
                if statuses and passed == len(statuses)
                else "INCOMPLETE"
            ),
            "total_metrics": len(statuses),
            "passed": passed,
            "failed": failed,
            "results": regression,
        }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)

    return report


if __name__ == "__main__":
    result = create_qa_report()

    print("=== Unified QA Report ===")
    print(
        "Speech benchmark:",
        result["speech_benchmark"]["status"],
    )
    print(
        "Speech samples:",
        result["speech_benchmark"]["sample_count"],
    )
    print(
        "Performance regression:",
        result["performance_regression"]["status"],
    )
    print(
        "Performance metrics:",
        result["performance_regression"]["total_metrics"],
    )
    print(f"Report saved to: {OUTPUT_FILE}")
    print("Pytest:", result["pytest"]["status"])
    print("Pytest passed:", result["pytest"]["passed"])
