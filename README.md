# Multilingual Voice QA Automation

[![Automated Tests](https://github.com/pdchoinyc/siri-voice-qa-automation/actions/workflows/pytest.yml/badge.svg)](https://github.com/pdchoinyc/siri-voice-qa-automation/actions/workflows/pytest.yml)

An independent Python QA engineering portfolio project that demonstrates multilingual voice-assistant testing, speech-to-text (STT) evaluation, rule-based intent validation, performance regression checks, and automated CI reporting.

> **Disclaimer:** This project is not affiliated with, endorsed by, or connected to Apple. It does not test Apple's Siri models, services, or proprietary systems. The intent classifier is a deliberately lightweight, rule-based test target—not a production NLU model.

## At a glance

| Area | Implementation |
| --- | --- |
| Languages | Korean (`ko-KR`), English (`en-US`), Japanese (`ja-JP`) |
| Intent labels | `WEATHER`, `TIMER`, `ALARM`, `UNKNOWN`, `MULTIPLE_INTENTS` |
| CI test suite | **51 passed, 4 deselected** in the latest verified GitHub Actions run |
| Local speech samples | Three recorded utterances, one per locale |
| STT engine | `faster-whisper`, multilingual Whisper Tiny, CPU inference |
| Quality metrics | WER, CER, intent prediction correctness |
| Performance metrics | Average latency, P95 latency, real-time factor (RTF) |
| Regression policy | Compare average and P95 latency against recorded baselines; flag regressions over 20% |
| Reporting | JUnit XML, pytest-html, CSV, unified JSON, standalone HTML dashboard |
| CI | GitHub Actions with downloadable report artifacts |

The latest CI run verifies code-based tests only. Speech inference and performance regression tests requiring local audio or benchmark data are **not executed in CI**.

## 1. Project objectives

- Design reproducible automated QA checks for a multilingual voice-assistant-style pipeline.
- Verify intent handling across supported languages, unknown requests, and invalid inputs.
- Measure transcription quality and identify downstream intent-classification failures.
- Benchmark local STT inference and detect latency regressions against a versioned baseline.
- Produce traceable test results and downloadable CI artifacts.
- Distinguish **passed**, **failed**, and **not run** checks in reports.

## 2. System architecture

### Text-based functional QA

```text
Text utterance
    -> Rule-based intent classifier
    -> Predicted intent
    -> Pytest assertions
    -> JUnit XML / pytest-html
```

### Local audio-based QA

```text
Recorded audio (local, not committed)
    -> faster-whisper STT
    -> Transcription
    -> WER / CER evaluation
    -> Rule-based intent classification
    -> Intent validation + latency / RTF measurements
    -> Benchmark CSV
    -> Baseline comparison / regression CSV
```

### Unified reporting

```text
Pytest JUnit XML -----------+
Speech benchmark CSV -------+--> generate_qa_report.py --> qa_summary.json
Performance regression CSV -+                               |
                                                            v
                                                generate_dashboard.py
                                                            |
                                                            v
                                                    qa_dashboard.html
```

The report generator marks unavailable speech and performance results as `NOT_RUN`, rather than treating missing evidence as a pass.

## 3. Technology stack

| Category | Technology |
| --- | --- |
| Language | Python 3.13 |
| Test framework | Pytest |
| STT inference | faster-whisper (Whisper Tiny) |
| Speech evaluation | JiWER |
| Intent classification | Rule-based keyword classifier |
| Performance analysis | Python, CSV, latency statistics, RTF |
| Reporting | pytest-html, JUnit XML, JSON, CSV, HTML |
| CI/CD | GitHub Actions, artifact uploads |
| Version control | Git and GitHub |

## 4. Test strategy and coverage

The CI-selected suite currently includes **51 automated tests**. It covers intent-classification behavior, multilingual text inputs, negative and boundary cases, speech-evaluation utilities, benchmark-data validation, performance-regression calculation logic, and dashboard generation.

The Pytest configuration deselects **four local-only tests** by default: three speech-inference tests and one performance-regression test. Therefore, **51 passed, 4 deselected** does not mean 55 tests were executed.

Key design choices:

- **Functional checks:** Assert expected intent labels for representative utterances and edge cases.
- **Negative checks:** Exercise unsupported requests, invalid input types, and invalid performance data.
- **Data integrity:** Detect missing or duplicate benchmark identifiers, locale mismatches, and invalid numeric metrics.
- **Regression checks:** Evaluate average and P95 latency relative to stored baselines.
- **Reporting checks:** Verify that the dashboard is generated, includes expected results, and fails clearly when its input is missing.

## 5. Local multilingual speech results

A small controlled local dataset contains one recorded weather-related utterance per locale. In the documented benchmark, each recording was measured over **10 runs after warm-up**.

| Locale | Avg latency (s) | P95 latency (s) | Avg RTF | WER | CER | Intent accuracy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `ko-KR` | 0.5547 | 0.5978 | 0.1791 | 0.00 | 0.00 | 1.00 |
| `en-US` | 0.5088 | 0.5928 | 0.1340 | 0.00 | 0.00 | 1.00 |
| `ja-JP` | 0.5379 | 0.7023 | 0.1280 | 0.00 | 0.00 | 1.00 |

**Interpretation:** All three recorded samples were transcribed correctly and mapped to the expected `WEATHER` intent in this local run. These results **do not establish general STT accuracy**, language-wide reliability, or production latency. Measurements depend on the input recordings, model configuration, hardware, and environment. With 10 measurements, the nearest-rank P95 corresponds to the maximum observed value.

### Performance regression

The project stores initial average and P95 latency baselines in `data/speech_performance_baseline.json` and uses a **20% maximum allowed regression**. The local regression report contained **6 passing metric comparisons** (two metrics per locale) when evaluated against the recorded benchmark. A 0% difference against the initial baseline is not evidence that future runs will show no regression.

## 6. QA case study: Japanese transcription error

**Expected transcription:** `今日の天気を教えて` (asking about today's weather)

**Observed transcription:** `今日の電気を教えて` (the word for “weather” was recognized as “electricity”)

**Observed impact:**

- Character Error Rate (CER): 11.11% in the documented case.
- Expected intent: `WEATHER`.
- Predicted intent: `UNKNOWN`.
- Result: `FAIL`.

**Investigation:** The issue was reproduced using the original audio. Increasing the Whisper beam size from 1 to 5 did not resolve it. A new recording of the utterance produced the expected transcription and intent with the same model configuration.

**Conclusion:** The case illustrates error propagation from STT into downstream intent classification. Audio characteristics may have contributed, but the available observations do not prove a definitive root cause.

## 7. Getting started (Windows / PowerShell)

### Prerequisites

- Python 3.13
- Git
- Windows PowerShell (commands below)

Clone the repository and create a virtual environment:

```powershell
git clone https://github.com/pdchoinyc/siri-voice-qa-automation.git
cd siri-voice-qa-automation
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Run the default CI-compatible test suite:

```powershell
python -m pytest -v
```

Generate a JUnit XML report, unified summary, and HTML dashboard:

```powershell
python -m pytest --junitxml=reports/pytest_results.xml --html=report.html --self-contained-html
python generate_qa_report.py
python generate_dashboard.py
start .\reports\qa_dashboard.html
```

The generated reports are local outputs and are excluded from version control. Without local benchmark and regression CSV files, their corresponding dashboard sections show `NOT_RUN`.

### Local speech and performance evaluation

Audio recordings referenced in `data/speech_test_data.json` are **not included in this repository**. To run audio-dependent checks, provide your own appropriately licensed/consented local recordings at the configured paths.

```powershell
python run_multilingual_speech_test.py
python run_speech_benchmark.py
python run_performance_regression.py
```

To run the otherwise-deselected local Pytest checks, select the relevant markers explicitly after preparing the required audio and benchmark inputs:

```powershell
python -m pytest -m speech -o addopts=""
python -m pytest -m performance -o addopts=""
```

Performance results should be interpreted with regard to the local machine, recording duration, and run-to-run variability.

## 8. GitHub Actions and artifacts

The workflow in `.github/workflows/pytest.yml` runs on pushes and pull requests targeting `main`, and supports manual dispatch.

It installs dependencies, executes the CI-selected Pytest suite, generates JUnit XML and pytest-html reports, builds the unified JSON report and HTML dashboard, and uploads two downloadable artifacts:

| Artifact | Contents |
| --- | --- |
| `qa-report` | `pytest_results.xml`, `qa_summary.json`, `qa_dashboard.html` |
| `pytest-html-report` | `report.html` |

Download artifacts from a completed run under the repository's [Actions tab](https://github.com/pdchoinyc/siri-voice-qa-automation/actions).

**Expected CI report behavior:** Pytest results reflect the current CI run; speech benchmark and performance regression sections are `NOT_RUN` because private local audio and benchmark outputs are not available to GitHub Actions.

## 9. Limitations and future improvements

- The speech dataset is intentionally small (one utterance per locale) and is not representative of diverse accents, speakers, acoustic conditions, or requests.
- The classifier uses keyword rules, not a learned NLU model.
- Current benchmark results are local-machine measurements, not cross-device or production service-level benchmarks.
- Japanese WER can be sensitive to tokenization; language-aware segmentation would improve interpretability.
- Expand test fixtures for noise, accents, multi-intent utterances, and error analysis.
- Add non-sensitive, redistributable audio fixtures for reproducible speech tests in CI.
- Consider larger model comparisons and more robust performance baselines with repeated independent runs.

## 10. Scope

This repository is a QA automation and test-design portfolio project inspired by general challenges in multilingual voice interfaces. It demonstrates testing methods and engineering tradeoffs; it does not claim production readiness or access to proprietary assistant infrastructure.
