
import json
from html import escape
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
SUMMARY_FILE = REPORT_DIR / "qa_summary.json"
OUTPUT_FILE = REPORT_DIR / "qa_dashboard.html"


def safe(value):
    return escape(str(value))


def create_dashboard(summary_file=None, output_file=None):
    summary_file = Path(summary_file) if summary_file is not None else SUMMARY_FILE
    output_file = Path(output_file) if output_file is not None else OUTPUT_FILE
    if not summary_file.is_file():
        raise FileNotFoundError(
            "QA summary not found. Run generate_qa_report.py first."
        )

    with summary_file.open("r", encoding="utf-8") as file:
        report = json.load(file)

    pytest = report["pytest"]
    speech = report["speech_benchmark"]
    performance = report["performance_regression"]

    speech_rows = ""
    for item in speech["results"]:
        speech_rows += (
            "<tr>"
            f"<td>{safe(item['locale'])}</td>"
            f"<td>{safe(item['avg_latency_seconds'])}</td>"
            f"<td>{safe(item['p95_latency_seconds'])}</td>"
            f"<td>{safe(item['avg_wer'])}</td>"
            f"<td>{safe(item['avg_cer'])}</td>"
            f"<td>{safe(item['intent_accuracy'])}</td>"
            "</tr>"
        )

    performance_rows = ""
    for item in performance["results"]:
        performance_rows += (
            "<tr>"
            f"<td>{safe(item['locale'])}</td>"
            f"<td>{safe(item['metric'])}</td>"
            f"<td>{safe(item['regression_percent'])}%</td>"
            f"<td>{safe(item['status'])}</td>"
            "</tr>"
        )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Multilingual Voice QA Dashboard</title>
<style>
* {{ box-sizing: border-box; }}
body {{
    margin: 0;
    background: #f4f6fb;
    color: #1e293b;
    font-family: Arial, sans-serif;
}}
.container {{
    max-width: 1100px;
    margin: 40px auto;
    padding: 0 20px;
}}
h1 {{ margin-bottom: 8px; }}
.subtitle {{ color: #64748b; margin-bottom: 30px; }}
.cards {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
}}
.card, .panel {{
    background: white;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.05);
}}
.card h2 {{
    font-size: 14px;
    color: #64748b;
    margin: 0 0 14px;
}}
.value {{ font-size: 32px; font-weight: bold; }}
.pass {{ color: #15803d; }}
.fail {{ color: #dc2626; }}
.panel {{ margin-top: 24px; overflow-x: auto; }}
table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 16px;
}}
th, td {{
    padding: 12px;
    border-bottom: 1px solid #e2e8f0;
    text-align: left;
}}
th {{ background: #f8fafc; }}
.footer {{
    color: #64748b;
    font-size: 12px;
    margin-top: 24px;
}}
</style>
</head>
<body>
<div class="container">
<h1>Multilingual Voice QA Dashboard</h1>
<p class="subtitle">Generated: {safe(report["generated_at"])}</p>

<div class="cards">
    <div class="card">
        <h2>Pytest</h2>
        <div class="value">{safe(pytest["passed"])} / {safe(pytest["total"])}</div>
        <p>Status: {safe(pytest["status"])}</p>
    </div>
    <div class="card">
        <h2>Speech Samples</h2>
        <div class="value">{safe(speech["sample_count"])}</div>
        <p>Status: {safe(speech["status"])}</p>
    </div>
    <div class="card">
        <h2>Performance Checks</h2>
        <div class="value">{safe(performance["passed"])} / {safe(performance["total_metrics"])}</div>
        <p>Status: {safe(performance["status"])}</p>
    </div>
</div>

<div class="panel">
    <h2>Speech Benchmark</h2>
    <table>
        <thead>
            <tr>
                <th>Locale</th>
                <th>Avg Latency (s)</th>
                <th>P95 (s)</th>
                <th>WER</th>
                <th>CER</th>
                <th>Intent Accuracy</th>
            </tr>
        </thead>
        <tbody>{speech_rows}</tbody>
    </table>
</div>

<div class="panel">
    <h2>Performance Regression</h2>
    <table>
        <thead>
            <tr>
                <th>Locale</th>
                <th>Metric</th>
                <th>Regression</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>{performance_rows}</tbody>
    </table>
</div>

<p class="footer">
Local benchmark results only. Not an official Apple or Siri test system.
</p>
</div>
</body>
</html>"""

    output_file.write_text(html, encoding="utf-8")
    print(f"Dashboard saved to: {output_file}")


if __name__ == "__main__":
    create_dashboard()
